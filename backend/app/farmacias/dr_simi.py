from urllib.parse import quote

import httpx

from app.modelos import Producto, ResultadoFarmacia

LIMITE = 8


class DrSimi:
    id = "dr_simi"
    nombre = "Dr. Simi"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        url = f"https://www.drsimi.cl/api/catalog_system/pub/products/search/{quote(consulta)}"
        try:
            respuesta = await cliente.get(url, params={"_from": 0, "_to": LIMITE - 1}, headers={"Accept": "application/json"})
            respuesta.raise_for_status()
            data = respuesta.json()
        except (httpx.HTTPError, ValueError):
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="La búsqueda pública de Dr. Simi no respondió.")

        if not isinstance(data, list) or not data:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en Dr. Simi.")

        productos: list[Producto] = []
        for item in data[:LIMITE]:
            oferta = (((item.get("items") or [{}])[0].get("sellers") or [{}])[0].get("commertialOffer") or {})
            precio = oferta.get("Price")
            lista = oferta.get("ListPrice")
            productos.append(Producto(
                nombre=item.get("productName") or "Medicamento",
                marca=item.get("brand"),
                principio=(item.get("Principio Activo") or [None])[0],
                precio=round(precio) if isinstance(precio, (int, float)) else None,
                precio_lista=round(lista) if isinstance(lista, (int, float)) else None,
                bioequivalente=(item.get("Bioequivalente") or [None])[0] == "SI",
                url=item.get("link"),
            ))
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
