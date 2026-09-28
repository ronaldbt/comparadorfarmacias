import asyncio
import re

import httpx

from app.farmacias.ahumada import Ahumada
from app.farmacias.base import HEADERS
from app.farmacias.cruz_verde import CruzVerde
from app.farmacias.dr_simi import DrSimi
from app.farmacias.easyfarma import EasyFarma
from app.farmacias.ecofarmacias import EcoFarmacias
from app.farmacias.farmex import Farmex
from app.farmacias.farmazon import Farmazon
from app.farmacias.fonasa import Fonasa
from app.farmacias.knop import Knop
from app.farmacias.labotika import LaBotika
from app.farmacias.novasalud import Novasalud
from app.farmacias.salcobrand import Salcobrand
from app.modelos import RespuestaBusqueda, ResultadoFarmacia

FUENTES = (
    Ahumada(),
    CruzVerde(),
    DrSimi(),
    Fonasa(),
    LaBotika(),
    Farmex(),
    EcoFarmacias(),
    EasyFarma(),
    Novasalud(),
    Farmazon(),
    Knop(),
    Salcobrand(),
)
CONSULTA = re.compile(r"^[\w\sáéíóúüñÁÉÍÓÚÜÑ.,%-]{2,80}$", re.UNICODE)


async def buscar(consulta: str) -> RespuestaBusqueda:
    q = " ".join(consulta.split())
    if not CONSULTA.fullmatch(q):
        raise ValueError("La consulta solo puede incluir letras, números y espacios.")

    async with httpx.AsyncClient(timeout=15, headers=HEADERS, follow_redirects=True) as cliente:
        crudos = await asyncio.gather(*(fuente.buscar(cliente, q) for fuente in FUENTES), return_exceptions=True)

    farmacias: list[ResultadoFarmacia] = []
    for fuente, crudo in zip(FUENTES, crudos, strict=True):
        if isinstance(crudo, ResultadoFarmacia):
            farmacias.append(crudo)
        else:
            farmacias.append(ResultadoFarmacia(
                id=fuente.id,
                nombre=fuente.nombre,
                estado="error",
                mensaje="La fuente falló antes de devolver precios.",
            ))
    return RespuestaBusqueda(consulta=q, farmacias=farmacias)
