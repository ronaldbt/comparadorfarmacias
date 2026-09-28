from urllib.parse import quote_plus, urljoin

import httpx
from bs4 import BeautifulSoup

from app.farmacias.base import pesos
from app.modelos import Producto, ResultadoFarmacia

BASE = "https://farmex.cl"
LIMITE = 16


class Farmex:
    id = "farmex"
    nombre = "Farmex"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        url = f"{BASE}/search?q={quote_plus(consulta)}&type=product"
        try:
            respuesta = await cliente.get(url, headers={"Accept": "text/html"})
            respuesta.raise_for_status()
        except httpx.HTTPError:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="Farmex no respondió.")

        sopa = BeautifulSoup(respuesta.text, "html.parser")
        productos: list[Producto] = []
        for ficha in sopa.select(".product-card-wrapper")[:LIMITE]:
            titulo = ficha.select_one("h3, .card__heading")
            precio = ficha.select_one(".price-item")
            enlace = ficha.select_one("a[href*='/products/']")
            valor = pesos(precio.get_text(" ", strip=True) if precio else "")
            nombre = titulo.get_text(" ", strip=True) if titulo else ""
            if not nombre or valor is None:
                continue
            href = (enlace.get("href") or "").split("?", 1)[0] if enlace else ""
            productos.append(Producto(
                nombre=nombre,
                precio=valor,
                url=urljoin(BASE, href) if href else None,
            ))
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en Farmex.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
