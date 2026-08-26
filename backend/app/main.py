"""Punto de entrada de la API de NotaryVerify (FastAPI)."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    routes_auditoria,
    routes_credenciales,
    routes_documentos,
    routes_identidades,
    routes_tramites,
    routes_verificacion,
)
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="NotaryVerify",
    description=(
        "Prototipo experimental de verificación multicapa de identidad para "
        "trámites notariales. Sistema exclusivamente académico: NO sustituye "
        "a Reniec, al SID-Sunarp ni a la firma digital oficial, y sus "
        "resultados no tienen valor de identificación legal."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_identidades.router)
app.include_router(routes_credenciales.router)
app.include_router(routes_verificacion.router)
app.include_router(routes_documentos.router)
app.include_router(routes_auditoria.router)
app.include_router(routes_tramites.router)


@app.get("/", tags=["Estado"])
def estado():
    return {
        "sistema": "NotaryVerify",
        "estado": "operativo",
        "aviso": "Prototipo académico sin valor de identificación legal.",
    }
