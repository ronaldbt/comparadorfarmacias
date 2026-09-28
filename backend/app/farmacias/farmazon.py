from urllib.parse import quote_plus, urljoin

import httpx
from bs4 import BeautifulSoup

from app.farmacias.base import pesos
from app.modelos import Producto, ResultadoFarmacia

BASE = "https://www.farmazon.cl"
LIMITE = 16


class Farmazon:
    id = "farmazon"
    nombre = "Farmazon"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        url = f"{BASE}/shop?search={quote_plus(consulta)}"
        try:
            respuesta = await cliente.get(url, headers={"Accept": "text/html"})
            respuesta.raise_for_status()
        except httpx.HTTPError:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="Farmazon no respondió.")

        sopa = BeautifulSoup(respuesta.text, "html.parser")
        productos: list[Producto] = []
        for ficha in sopa.select("form.oe_product_cart")[:LIMITE]:
            enlace = ficha.select_one(".o_wsale_products_item_title a")
            valor_txt = ficha.select_one(".oe_currency_value")
            nombre = enlace.get_text(" ", strip=True) if enlace else ""
            valor = pesos(valor_txt.get_text(" ", strip=True) if valor_txt else "")
            if not nombre or valor is None:
                continue
            href = enlace.get("href") if enlace else ""
            productos.append(Producto(nombre=nombre, precio=valor, url=urljoin(BASE, href) if href else None))
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en Farmazon.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
