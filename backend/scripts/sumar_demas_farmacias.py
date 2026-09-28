"""Suma al catálogo el precio real de las farmacias que todavía no están en cada remedio."""

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.farmacias.ahumada import Ahumada
from app.farmacias.base import HEADERS
from app.farmacias.easyfarma import EasyFarma
from app.farmacias.ecofarmacias import EcoFarmacias
from app.farmacias.farmex import Farmex
from app.farmacias.farmazon import Farmazon
from app.farmacias.fonasa import Fonasa
from app.farmacias.labotika import LaBotika
from app.farmacias.novasalud import Novasalud
from sumar_knop_salcobrand import CATALOGO, consulta_busqueda, elegir

FUENTES = (
    (Ahumada(), "Ahumada"),
    (Fonasa(), "Fonasa"),
    (LaBotika(), "La Botika"),
    (Farmex(), "Farmex"),
    (EcoFarmacias(), "EcoFarmacias"),
    (EasyFarma(), "EasyFarma"),
    (Novasalud(), "Novasalud"),
    (Farmazon(), "Farmazon"),
)


async def oferta_de(cliente: httpx.AsyncClient, fuente, etiqueta: str, producto: dict) -> dict | None:
    try:
        resultado = await fuente.buscar(cliente, consulta_busqueda(producto)[:80])
    except Exception:
        return None
    if resultado.estado != "ok":
        return None
    filas = []
    for item in resultado.productos:
        fila = item.model_dump()
        fila["nombre"] = " ".join(parte for parte in (fila.get("nombre"), fila.get("presentacion")) if parte)
        filas.append(fila)
    elegido = elegir(filas, producto["nombre"])
    if not elegido or not elegido.get("precio"):
        return None
    return {
        "farmacia": etiqueta,
        "precio": elegido["precio"],
        "detalle": elegido.get("nombre"),
        "url": elegido.get("url"),
    }


async def main() -> None:
    data = json.loads(CATALOGO.read_text(encoding="utf-8"))
    productos = data["productos"]
    semaforo = asyncio.Semaphore(8)
    candado = asyncio.Lock()
    nuevos = {etiqueta: 0 for _fuente, etiqueta in FUENTES}
    hechos = 0

    def guardar() -> None:
        data["actualizado"] = datetime.now(timezone.utc).isoformat()
        CATALOGO.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    async with httpx.AsyncClient(timeout=25, headers=HEADERS, follow_redirects=True) as cliente:
        async def pedir(fuente, etiqueta: str, producto: dict) -> dict | None:
            async with semaforo:
                oferta = await oferta_de(cliente, fuente, etiqueta, producto)
                await asyncio.sleep(0.05)
                return oferta

        async def uno(indice: int, producto: dict) -> None:
            nonlocal hechos
            presentes = {oferta["farmacia"] for oferta in producto["ofertas"]}
            pendientes = [(fuente, etiqueta) for fuente, etiqueta in FUENTES if etiqueta not in presentes]
            agregadas = [oferta for oferta in await asyncio.gather(*(pedir(fuente, etiqueta, producto) for fuente, etiqueta in pendientes)) if oferta]
            async with candado:
                if agregadas:
                    producto["ofertas"].extend(agregadas)
                    producto["ofertas"].sort(key=lambda oferta: oferta["precio"])
                    for oferta in agregadas:
                        nuevos[oferta["farmacia"]] += 1
                hechos += 1
                if hechos % 15 == 0:
                    guardar()
                    print(hechos, producto["nombre"], [f"{o['farmacia']} {o['precio']}" for o in producto["ofertas"]], flush=True)

        def turno(i: int) -> tuple[int, int]:
            producto = productos[i]
            cantidad = len(producto["ofertas"])
            if producto.get("destacado"):
                return (0, cantidad)
            if cantidad == 2:
                return (1, 0)
            return (2, cantidad)

        orden = sorted(range(len(productos)), key=turno)
        await asyncio.gather(*(uno(i, productos[i]) for i in orden))

    guardar()
    print("guardado", nuevos)


if __name__ == "__main__":
    asyncio.run(main())
