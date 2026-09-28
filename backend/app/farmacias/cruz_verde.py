import httpx

from app.modelos import ResultadoFarmacia


class CruzVerde:
    id = "cruz_verde"
    nombre = "Cruz Verde"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        try:
            respuesta = await cliente.get("https://www.cruzverde.cl/", headers={"Accept": "text/html"})
        except httpx.HTTPError:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="Cruz Verde no respondió.")

        html = respuesta.text
        tiene_precios = "product-tile" in html or "itemprop=\"price\"" in html
        if respuesta.status_code >= 400 or not tiene_precios:
            return ResultadoFarmacia(
                id=self.id,
                nombre=self.nombre,
                estado="sin_precio_publico",
                mensaje="Cruz Verde no publica los precios en el HTML. El motor no evade el control anti-bot.",
            )
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados")
