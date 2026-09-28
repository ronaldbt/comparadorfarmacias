import re
from urllib.parse import quote_plus, urljoin

import httpx
from bs4 import BeautifulSoup

from app.modelos import Producto, ResultadoFarmacia

BASE = "https://www.farmaciasahumada.cl"
LIMITE = 12


def _precio(texto: str) -> int | None:
    encontrado = re.search(r"\$\s*([\d.]+)", texto)
    if not encontrado:
        return None
    digitos = encontrado.group(1).replace(".", "")
    return int(digitos) if digitos.isdigit() else None


class Ahumada:
    id = "ahumada"
    nombre = "Farmacias Ahumada"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        url = f"{BASE}/search?q={quote_plus(consulta)}"
        try:
            respuesta = await cliente.get(url, headers={"Accept": "text/html"})
        except httpx.HTTPError:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="Ahumada no respondió.")

        html = respuesta.text
        if respuesta.status_code >= 400 or "Just a moment" in html or "cf-browser-verification" in html:
            return ResultadoFarmacia(
                id=self.id,
                nombre=self.nombre,
                estado="sin_precio_publico",
                mensaje="Ahumada no entregó la página de búsqueda.",
            )

        productos = _productos(html)
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en Ahumada.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)


def _productos(html: str) -> list[Producto]:
    sopa = BeautifulSoup(html, "html.parser")
    productos: list[Producto] = []
    for ficha in sopa.select(".product-tile")[:LIMITE]:
        enlace = ficha.select_one(".pdp-link a")
        if enlace is None:
            continue
        nombre = enlace.get_text(strip=True)
        if not nombre:
            continue
        href = enlace.get("href") or ""
        marca = ficha.select_one(".product-tile-brand")
        venta = ficha.select_one(".sales")
        lista = ficha.select_one(".strike-through .value")
        precio_lista = None
        if lista is not None and str(lista.get("content") or "").isdigit():
            precio_lista = int(str(lista.get("content")))
        precio = _precio(venta.get_text(" ", strip=True)) if venta else None
        productos.append(Producto(
            nombre=nombre,
            marca=marca.get_text(strip=True) if marca else None,
            precio=precio if precio is not None else precio_lista,
            precio_lista=precio_lista,
            bioequivalente=ficha.select_one(".bioequivalent-badge") is not None,
            url=urljoin(BASE, href) if href else None,
        ))
    return productos
