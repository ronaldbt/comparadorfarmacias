from urllib.parse import quote_plus

import httpx

from app.modelos import Producto, ResultadoFarmacia

LIMITE = 16


class EasyFarma:
    id = "easyfarma"
    nombre = "EasyFarma"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        url = f"https://www.easyfarma.cl/busqueda?s={quote_plus(consulta)}"
        try:
            respuesta = await cliente.get(url, headers={"Accept": "application/json"})
            respuesta.raise_for_status()
            data = respuesta.json()
        except (httpx.HTTPError, ValueError):
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="EasyFarma no respondió.")

        productos: list[Producto] = []
        for item in (data.get("products") or [])[:LIMITE]:
            valor = item.get("price_amount")
            if not isinstance(valor, (int, float)) or valor <= 0:
                continue
            productos.append(Producto(
                nombre=item.get("name") or "Medicamento",
                marca=item.get("manufacturer_name") or None,
                precio=round(valor),
                url=item.get("url") or item.get("link"),
            ))
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en EasyFarma.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
