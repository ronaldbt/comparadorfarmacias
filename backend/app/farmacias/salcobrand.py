import httpx

from app.modelos import Producto, ResultadoFarmacia

APP = "GM3RP06HJG"
# Clave de búsqueda pública que el sitio carga en el navegador. Solo puede consultar el índice de productos.
CLAVE = "0259fe250b3be4b1326eb85e47aa7d81"
INDICE = "sb_variant_production"
LIMITE = 16


class Salcobrand:
    id = "salcobrand"
    nombre = "Salcobrand"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        url = f"https://{APP}-dsn.algolia.net/1/indexes/{INDICE}/query"
        try:
            respuesta = await cliente.post(
                url,
                headers={
                    "x-algolia-application-id": APP,
                    "x-algolia-api-key": CLAVE,
                    "Referer": "https://salcobrand.cl/",
                    "Origin": "https://salcobrand.cl",
                },
                json={"query": consulta, "hitsPerPage": LIMITE},
            )
            respuesta.raise_for_status()
            data = respuesta.json()
        except (httpx.HTTPError, ValueError):
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="Salcobrand no respondió.")

        productos: list[Producto] = []
        for item in data.get("hits") or []:
            normal = item.get("normal_price")
            internet = item.get("direct_discount")
            try:
                precio_farmacia = int(normal) if normal not in (None, "") else None
            except (TypeError, ValueError):
                precio_farmacia = None
            try:
                precio_internet = int(float(internet)) if internet not in (None, "") else None
            except (TypeError, ValueError):
                precio_internet = None
            precio = precio_internet or precio_farmacia
            if not precio or precio <= 0:
                continue
            bio = item.get("bioequivalent_filter") or {}
            slug = item.get("slug")
            productos.append(Producto(
                nombre=item.get("name") or "Medicamento",
                marca=item.get("brand") or None,
                precio=precio,
                precio_lista=precio_farmacia if precio_farmacia and precio_farmacia != precio else None,
                bioequivalente=bio.get("has_bioequivalent") if isinstance(bio, dict) else None,
                url=f"https://salcobrand.cl/products/{slug}" if slug else None,
            ))
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en Salcobrand.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
