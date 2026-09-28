from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.motor import buscar

app = FastAPI(title="Salvia comparador", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/salud")
def salud() -> dict[str, bool]:
    return {"ok": True}


@app.get("/buscar")
async def buscar_medicamento(q: str = Query(min_length=2, max_length=80)):
    try:
        return await buscar(q)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
