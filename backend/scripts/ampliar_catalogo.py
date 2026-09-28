"""Agrega medicamentos con el precio público de Dr. Simi. No inventa otros precios."""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

CATALOGO = Path(__file__).resolve().parents[2] / "frontend" / "app" / "data" / "catalogo.json"
BUSQUEDA = "https://www.drsimi.cl/api/catalog_system/pub/products/search"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}


def precio_real(item: dict) -> int | None:
    oferta = (((item.get("items") or [{}])[0].get("sellers") or [{}])[0].get("commertialOffer") or {})
    valor = oferta.get("Price")
    if not isinstance(valor, (int, float)) or valor <= 0:
        return None
    return round(valor)


def main() -> None:
    guardado = json.loads(CATALOGO.read_text(encoding="utf-8"))
    productos = list(guardado.get("productos") or [])
    urls = {
        oferta.get("url")
        for producto in productos
        for oferta in producto.get("ofertas") or []
        if oferta.get("url")
    }

    agregados = 0
    inicio = 0
    total = None
    with httpx.Client(timeout=30, headers=HEADERS, follow_redirects=True) as cliente:
        while total is None or inicio < total:
            try:
                respuesta = cliente.get(BUSQUEDA, params={"fq": "C:/147/", "_from": inicio, "_to": inicio + 49})
                respuesta.raise_for_status()
            except httpx.HTTPError as exc:
                print("reintento", inicio, exc, flush=True)
                time.sleep(2)
                respuesta = cliente.get(BUSQUEDA, params={"fq": "C:/147/", "_from": inicio, "_to": inicio + 49})
                if respuesta.status_code >= 400:
                    print("se corta en", inicio, respuesta.status_code, flush=True)
                    break
            if total is None:
                recursos = respuesta.headers.get("resources", "")
                total = int(recursos.rsplit("/", 1)[-1]) if "/" in recursos else 0
                print("catalogo publico", total, flush=True)
            pagina = respuesta.json()
            if not isinstance(pagina, list) or not pagina:
                break
            for item in pagina:
                valor = precio_real(item)
                enlace = item.get("link")
                nombre = (item.get("productName") or "").strip()
                if valor is None or not enlace or not nombre or enlace in urls:
                    continue
                urls.add(enlace)
                productos.append({
                    "id": f"simi-{item.get('productId') or agregados}",
                    "nombre": nombre,
                    "marca": item.get("brand") or None,
                    "consulta": nombre,
                    "destacado": False,
                    "ofertas": [{
                        "farmacia": "Dr. Simi",
                        "precio": valor,
                        "detalle": nombre,
                        "url": enlace,
                    }],
                })
                agregados += 1
            inicio += 50
            print("leidos", inicio, "agregados", agregados, flush=True)
            time.sleep(0.4)
            if inicio > 2000:
                break

    CATALOGO.write_text(json.dumps({
        "actualizado": datetime.now(timezone.utc).isoformat(),
        "productos": productos,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("total", len(productos), "nuevos", agregados)


if __name__ == "__main__":
    main()
