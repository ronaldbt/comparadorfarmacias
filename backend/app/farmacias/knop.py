import httpx

from app.modelos import Producto, ResultadoFarmacia

LIMITE = 16


class Knop:
    id = "knop"
    nombre = "Farmacias Knop"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        try:
            respuesta = await cliente.get(
                "https://www.farmaciasknop.com/products.json",
                params={"q": consulta, "limit": LIMITE},
                headers={"Accept": "application/json"},
            )
            respuesta.raise_for_status()
            data = respuesta.json()
        except (httpx.HTTPError, ValueError):
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="Farmacias Knop no respondió.")

        productos: list[Producto] = []
        for item in (data.get("products") or [])[:LIMITE]:
            venta = item.get("sale_price")
            normal = item.get("price")
            try:
                precio = int(venta if isinstance(venta, (int, float)) and venta > 0 else normal)
            except (TypeError, ValueError):
                continue
            if precio <= 0:
                continue
            lista = item.get("regular_price")
            precio_lista = int(lista) if isinstance(lista, (int, float)) and int(lista) > precio else None
            vendedor = item.get("vendor")
            marca = vendedor.get("name") if isinstance(vendedor, dict) else vendedor if isinstance(vendedor, str) else None
            productos.append(Producto(
                nombre=item.get("name") or "Medicamento",
                marca=marca or None,
                precio=precio,
                precio_lista=precio_lista,
                url=item.get("url"),
            ))
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en Farmacias Knop.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
