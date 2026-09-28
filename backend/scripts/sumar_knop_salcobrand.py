"""Agrega a cada remedio del catálogo el precio real de Knop y Salcobrand, si existe un producto comparable."""

import asyncio
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.farmacias.base import HEADERS
from app.farmacias.knop import Knop
from app.farmacias.salcobrand import Salcobrand

CATALOGO = Path(__file__).resolve().parents[2] / "frontend" / "app" / "data" / "catalogo.json"
ETIQUETAS = {"knop": "Knop", "salcobrand": "Salcobrand"}
FORMAS = {
    "comprimidos", "comprimido", "capsulas", "capsula", "crema", "jarabe", "suspension",
    "inyectable", "gramos", "gramo", "caja", "sobre", "sobres", "gel", "unguento",
    "solucion", "oral", "topica", "topico", "recubiertos", "recubierto", "tabletas",
    "tableta", "unidades", "unidad", "dosis", "aerosol", "gotas", "ampolla", "ampollas",
}
STOP = FORMAS | {
    "para", "con", "como", "desde", "agua", "regular", "sabor", "adulto", "infantil",
    "compuesto", "compuesta", "pack", "plus", "uso", "cada", "este", "esta", "unos",
    "unas", "limon", "naranja", "menta", "mentol", "frasco", "tubo", "aceite", "fruta",
    "frutas", "natural", "organico", "sal",
}
PRESENTACIONES = (
    "supositorio", "jarabe", "crema", "aerosol", "unguento", "emulsion", "laca",
    "shampoo", "comprimido", "capsula", "gota", "tableta", "ampolla", "sobre",
)
FUERZA = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:mg|mcg|ui|%)")
CONTEO = re.compile(
    r"(\d+)\s*(?:comprimidos?|c[aá]psulas?|capsulas?|tabletas?|dosis|ampollas?|sobres?|ml|g)\b",
    re.I,
)


def normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFD", (texto or "").lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def conteo_de(texto: str) -> str | None:
    sin_fuerza = FUERZA.sub(" ", normalizar(texto))
    hallado = CONTEO.search(sin_fuerza)
    return hallado.group(1) if hallado else None


def analizar(texto: str) -> tuple[list[str], list[str], str | None]:
    limpio = normalizar(texto)
    tokens = [parte for parte in re.split(r"[^a-z0-9]+", limpio) if parte]
    palabras = [parte for parte in tokens if parte.isalpha() and len(parte) > 3 and parte not in FORMAS]
    fuerzas = [numero.split(".")[0] for numero in FUERZA.findall(limpio)]
    return palabras, fuerzas, conteo_de(texto)


def identidad(texto: str) -> str | None:
    tokens = [parte for parte in re.split(r"[^a-z0-9]+", normalizar(texto)) if parte.isalpha()]
    for token in tokens:
        if len(token) >= 4 and token not in STOP:
            return token
    return None


def presentacion(texto: str) -> str | None:
    limpio = normalizar(texto)
    for forma in PRESENTACIONES:
        if forma in limpio:
            return forma
    return None


def aceptable(referencia: str, detalle: str) -> bool:
    clave = identidad(referencia)
    nombre = normalizar(detalle or "")
    if not clave or not re.search(rf"(?<![a-z]){re.escape(clave)}(?![a-z])", nombre):
        return False
    if "/" in (detalle or "") and "/" not in referencia:
        return False
    forma = presentacion(referencia)
    if forma and presentacion(detalle or "") != forma:
        return False
    _palabras, fuerzas, conteo = analizar(referencia)
    if fuerzas and not all(re.search(rf"(?<!\d){numero}(?!\d)", nombre) for numero in fuerzas):
        return False
    conteo_hallado = conteo_de(detalle or "")
    if conteo and conteo_hallado and conteo_hallado != conteo:
        return False
    return True


def consulta_busqueda(producto: dict) -> str:
    texto = (producto.get("consulta") or "").strip()
    if texto and len(texto.split()) <= 4:
        return texto
    palabras, fuerzas, _conteo = analizar(producto.get("nombre") or texto)
    partes = (palabras[:1] + fuerzas[:1]) or texto.split()[:3]
    return " ".join(partes)[:80]


def elegir(productos: list[dict], referencia: str) -> dict | None:
    palabras, fuerzas, conteo = analizar(referencia)
    if not palabras:
        return None
    candidatos = []
    for producto in productos:
        if not producto.get("precio"):
            continue
        crudo = producto.get("nombre") or ""
        nombre = normalizar(crudo)
        if any(marca in nombre for marca in ("arrugad", "vencid", "merma")):
            continue
        if not any(re.search(rf"(?<![a-z]){re.escape(palabra)}(?![a-z])", nombre) for palabra in palabras):
            continue
        if "/" in crudo and "/" not in referencia:
            continue
        if fuerzas and not all(re.search(rf"(?<!\d){numero}(?!\d)", nombre) for numero in fuerzas):
            continue
        conteo_hallado = conteo_de(crudo)
        if conteo and conteo_hallado and conteo_hallado != conteo:
            continue
        coincidencias = sum(1 for palabra in palabras if re.search(rf"(?<![a-z]){re.escape(palabra)}(?![a-z])", nombre))
        candidatos.append((producto["precio"], -coincidencias, producto))
    if not candidatos:
        return None
    candidatos.sort(key=lambda item: (item[0], item[1]))
    elegido = candidatos[0][2]
    if not aceptable(referencia, elegido.get("nombre") or ""):
        return None
    return elegido


async def buscar_fuente(cliente: httpx.AsyncClient, fuente, busqueda: str, referencia: str) -> dict | None:
    try:
        resultado = await fuente.buscar(cliente, busqueda[:80])
    except Exception:
        return None
    if resultado.estado != "ok":
        return None
    elegido = elegir([item.model_dump() for item in resultado.productos], referencia)
    if not elegido:
        return None
    return {
        "farmacia": ETIQUETAS[fuente.id],
        "precio": elegido["precio"],
        "detalle": elegido.get("nombre"),
        "url": elegido.get("url"),
    }


async def main() -> None:
    data = json.loads(CATALOGO.read_text(encoding="utf-8"))
    productos = data["productos"]
    fuentes = (Knop(), Salcobrand())
    semaforo = asyncio.Semaphore(3)
    nuevos = {"Knop": 0, "Salcobrand": 0}

    async with httpx.AsyncClient(timeout=20, headers=HEADERS, follow_redirects=True) as cliente:
        async def uno(indice: int, producto: dict) -> None:
            async with semaforo:
                ofertas = [oferta for oferta in producto["ofertas"] if oferta["farmacia"] not in ETIQUETAS.values()]
                for fuente in fuentes:
                    oferta = await buscar_fuente(cliente, fuente, consulta_busqueda(producto), producto["nombre"])
                    if oferta:
                        ofertas.append(oferta)
                        nuevos[oferta["farmacia"]] += 1
                    await asyncio.sleep(0.15)
                ofertas.sort(key=lambda oferta: oferta["precio"])
                producto["ofertas"] = ofertas
                if indice % 40 == 0:
                    print(indice, producto["nombre"], [f"{o['farmacia']} {o['precio']}" for o in ofertas], flush=True)

        await asyncio.gather(*(uno(i, producto) for i, producto in enumerate(productos)))

    data["actualizado"] = datetime.now(timezone.utc).isoformat()
    CATALOGO.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("guardado", nuevos)


if __name__ == "__main__":
    asyncio.run(main())
