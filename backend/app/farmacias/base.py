from typing import Protocol

import httpx

from app.modelos import ResultadoFarmacia

import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept-Language": "es-CL,es;q=0.9",
}


def pesos(texto: str) -> int | None:
    digitos = re.sub(r"[^\d]", "", texto or "")
    return int(digitos) if digitos else None


class Farmacia(Protocol):
    id: str
    nombre: str

    async def buscar(self, cliente: httpx.AsyncClient, consulta: str) -> ResultadoFarmacia:
        ...
