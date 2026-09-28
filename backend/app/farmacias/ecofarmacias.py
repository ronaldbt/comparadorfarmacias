import httpx

from app.modelos import Producto, ResultadoFarmacia

LIMITE = 16


class EcoFarmacias:
    id = "ecofarmacias"
    nombre = "EcoFarmacias"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        url = "https://www.ecofarmacias.cl/wp-json/wc/store/v1/products"
        try:
            respuesta = await cliente.get(
                url,
                params={"search": consulta, "per_page": LIMITE},
                headers={"Accept": "application/json"},
            )
            respuesta.raise_for_status()
            data = respuesta.json()
        except (httpx.HTTPError, ValueError):
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="EcoFarmacias no respondió.")

        productos: list[Producto] = []
        for item in data if isinstance(data, list) else []:
            precios = item.get("prices") or {}
            try:
                valor = int(precios.get("price"))
            except (TypeError, ValueError):
                continue
            if valor <= 0:
                continue
            productos.append(Producto(
                nombre=item.get("name") or "Medicamento",
                precio=valor,
                url=item.get("permalink"),
            ))
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en EcoFarmacias.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
