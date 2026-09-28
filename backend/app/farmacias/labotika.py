from urllib.parse import quote_plus, urljoin

import httpx

from app.modelos import Producto, ResultadoFarmacia

BASE = "https://farmacialabotika.cl"
LIMITE = 16


class LaBotika:
    id = "labotika"
    nombre = "Farmacia La Botika"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        url = f"{BASE}/search/suggest.json?q={quote_plus(consulta)}&resources[type]=product&resources[limit]={LIMITE}"
        try:
            respuesta = await cliente.get(url, headers={"Accept": "application/json"})
            respuesta.raise_for_status()
            data = respuesta.json()
        except (httpx.HTTPError, ValueError):
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="La Botika no respondió.")

        crudos = (((data.get("resources") or {}).get("results") or {}).get("products") or [])
        productos: list[Producto] = []
        for item in crudos[:LIMITE]:
            try:
                precio = int(item.get("price"))
            except (TypeError, ValueError):
                continue
            if precio <= 0:
                continue
            enlace = item.get("url") or ""
            productos.append(Producto(
                nombre=item.get("title") or "Medicamento",
                marca=item.get("vendor") or None,
                precio=precio,
                url=urljoin(BASE, enlace.split("?", 1)[0]) if enlace else None,
            ))
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Sin resultados en La Botika.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
