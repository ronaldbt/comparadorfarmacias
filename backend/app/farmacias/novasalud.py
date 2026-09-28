from urllib.parse import quote_plus, urljoin

import httpx
from bs4 import BeautifulSoup

from app.farmacias.base import pesos
from app.modelos import Producto, ResultadoFarmacia

BASE = "https://www.novasalud.cl"
LIMITE = 16


class Novasalud:
    id = "novasalud"
    nombre = "Novasalud"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        url = f"{BASE}/catalogsearch/result/?q={quote_plus(consulta)}"
        try:
            respuesta = await cliente.get(url, headers={"Accept": "text/html"}, timeout=25)
            respuesta.raise_for_status()
        except httpx.HTTPError:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="Novasalud no respondió.")

        sopa = BeautifulSoup(respuesta.text, "html.parser")
        productos: list[Producto] = []
        for ficha in sopa.select(".product-item")[:LIMITE]:
            enlace = ficha.select_one(".product-item-link")
            precio = ficha.select_one(".special-price .price") or ficha.select_one(".price")
            nombre = enlace.get_text(" ", strip=True) if enlace else ""
            valor = pesos(precio.get_text(" ", strip=True) if precio else "")
            if not nombre or valor is None:
                continue
            href = enlace.get("href") if enlace else ""
            productos.append(Producto(nombre=nombre, precio=valor, url=urljoin(BASE, href) if href else None))
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en Novasalud.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
