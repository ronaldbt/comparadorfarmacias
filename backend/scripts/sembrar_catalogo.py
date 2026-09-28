"""Arma el catálogo de la portada consultando el motor, una búsqueda a la vez."""

import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CONSULTAS = [
    ("paracetamol-500", "paracetamol 500", True),
    ("ibuprofeno-400", "ibuprofeno 400", True),
    ("omeprazol-20", "omeprazol 20", True),
    ("losartan-50", "losartan 50", True),
    ("loratadina-10", "loratadina 10", True),
    ("amoxicilina-500", "amoxicilina 500", True),
    ("metformina-850", "metformina 850", True),
    ("atorvastatina-20", "atorvastatina 20", True),
    ("cetirizina-10", "cetirizina 10", False),
    ("enalapril-10", "enalapril 10", False),
    ("salbutamol", "salbutamol", False),
    ("levotiroxina-100", "levotiroxina 100", False),
    ("ketorolaco", "ketorolaco", False),
    ("sertralina-50", "sertralina 50", False),
    ("esomeprazol", "esomeprazol", False),
    ("clorfenamina", "clorfenamina", False),
]

SALIDA = Path(__file__).resolve().parents[2] / "frontend" / "app" / "data" / "catalogo.json"
NOMBRES = {"ahumada": "Ahumada", "dr_simi": "Dr. Simi", "fonasa": "Fonasa"}


def elegir(productos: list[dict], consulta: str) -> dict | None:
    tokens = [parte for parte in consulta.lower().split() if not parte.isdigit()]
    dosis = [parte for parte in consulta.lower().split() if parte.isdigit()]
    principal = tokens[0] if tokens else ""
    candidatos = []
    for producto in productos:
        if not producto.get("precio"):
            continue
        nombre = (producto.get("nombre") or "").lower()
        principio = (producto.get("principio") or "").lower()
        texto = f"{nombre} {principio} {(producto.get('presentacion') or '').lower()}"
        if principal and principal not in texto:
            continue
        prioridad = 0 if dosis and any(numero in texto for numero in dosis) else 1
        if nombre.startswith(principal):
            prioridad -= 1
        candidatos.append((prioridad, producto["precio"], producto))
    if not candidatos:
        return None
    candidatos.sort(key=lambda item: (item[0], item[1]))
    return candidatos[0][2]


def buscar(consulta: str) -> dict:
    url = "http://127.0.0.1:8000/buscar?" + urllib.parse.urlencode({"q": consulta})
    with urllib.request.urlopen(url, timeout=40) as respuesta:
        return json.load(respuesta)


def main() -> None:
    productos = []
    for identificador, consulta, destacado in CONSULTAS:
        print("buscando", consulta, flush=True)
        try:
            data = buscar(consulta)
        except Exception as exc:
            print("  fallo", exc)
            time.sleep(1)
            continue
        ofertas = []
        nombre = None
        marca = None
        for fuente in data.get("farmacias") or []:
            etiqueta = NOMBRES.get(fuente.get("id"))
            if not etiqueta:
                continue
            elegido = elegir(fuente.get("productos") or [], consulta)
            if not elegido:
                continue
            ofertas.append({
                "farmacia": etiqueta,
                "precio": elegido["precio"],
                "detalle": elegido.get("nombre"),
                "url": elegido.get("url"),
            })
            if nombre is None:
                nombre = elegido.get("nombre")
                marca = elegido.get("marca") or elegido.get("laboratorio")
        if len(ofertas) < 1 or not nombre:
            print("  sin precio")
            time.sleep(1)
            continue
        ofertas.sort(key=lambda oferta: oferta["precio"])
        productos.append({
            "id": identificador,
            "nombre": nombre,
            "marca": marca,
            "consulta": consulta,
            "destacado": destacado,
            "ofertas": ofertas,
        })
        print("  ", nombre, [f"{o['farmacia']} {o['precio']}" for o in ofertas])
        time.sleep(1.2)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps({
        "actualizado": datetime.now(timezone.utc).isoformat(),
        "productos": productos,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("guardado", SALIDA, "productos", len(productos))


if __name__ == "__main__":
    main()
