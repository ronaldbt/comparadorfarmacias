import httpx

from app.modelos import Producto, ResultadoFarmacia

SANTIAGO = ("-33.4489", "-70.6693")
LIMITE = 12


class Fonasa:
    id = "fonasa"
    nombre = "Convenio Fonasa"

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        try:
            respuesta = await cliente.post(
                "https://api.fonasa.cl/medicamentos/obtener",
                headers={
                    "Accept": "application/json",
                    "Origin": "https://medicamentos.fonasa.cl",
                    "Referer": "https://medicamentos.fonasa.cl/",
                },
                json={
                    "latitud": SANTIAGO[0],
                    "longitud": SANTIAGO[1],
                    "nombreMedicamento": consulta,
                    "principioActivo": None,
                },
            )
            respuesta.raise_for_status()
            data = respuesta.json()
        except (httpx.HTTPError, ValueError):
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="error", mensaje="Fonasa no respondió.")

        productos: list[Producto] = []
        for grupo in data.get("listado") or []:
            for presentacion in grupo.get("presentacionesExistentes") or []:
                for item in presentacion.get("productos") or []:
                    oferta = item.get("ofertaFonasa")
                    try:
                        precio = round(float(str(oferta).replace(",", "."))) if oferta not in (None, "") else None
                    except ValueError:
                        precio = None
                    equivalencia = (item.get("equivalencia") or "").upper()
                    productos.append(Producto(
                        nombre=item.get("nombreMedicamento") or consulta,
                        laboratorio=item.get("laboratorio"),
                        principio=item.get("principioActivo1"),
                        presentacion=item.get("presentacion"),
                        precio=precio,
                        bioequivalente="BIO" in equivalencia or "EQUIVALENTE" in equivalencia,
                    ))
                    if len(productos) >= LIMITE:
                        break
                if len(productos) >= LIMITE:
                    break
            if len(productos) >= LIMITE:
                break

        productos.sort(key=lambda producto: producto.precio if producto.precio is not None else 10**12)
        if not productos:
            return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="sin_resultados", mensaje="Fonasa no devolvió presentaciones.")
        return ResultadoFarmacia(id=self.id, nombre=self.nombre, estado="ok", productos=productos)
