from typing import Literal

from pydantic import BaseModel, Field


Estado = Literal["ok", "sin_resultados", "sin_precio_publico", "error"]


class Producto(BaseModel):
    nombre: str
    marca: str | None = None
    principio: str | None = None
    presentacion: str | None = None
    laboratorio: str | None = None
    precio: int | None = None
    precio_lista: int | None = None
    bioequivalente: bool | None = None
    url: str | None = None


class ResultadoFarmacia(BaseModel):
    id: str
    nombre: str
    estado: Estado
    mensaje: str | None = None
    productos: list[Producto] = Field(default_factory=list)


class RespuestaBusqueda(BaseModel):
    consulta: str
    farmacias: list[ResultadoFarmacia]
