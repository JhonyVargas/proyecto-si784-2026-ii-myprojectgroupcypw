"""Punto de entrada de la API de NotaryVerify (FastAPI)."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import (
    routes_auditoria,
    routes_auth,
    routes_credenciales,
    routes_documentos,
    routes_identidades,
    routes_tramites,
    routes_verificacion,
)
from app.core.database import init_db
from app.services.errors import (
    ConsentimientoRequeridoError, CredencialNoRegistradaError, DocumentoNoEncontradoError,
    IdentidadNoEncontradaError, NotaryVerifyError, RostroNoDetectadoError,
    SesionNoEncontradaError, SesionNoVigenteError, TramiteNoHabilitadoError,
)


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
app.include_router(routes_auth.router)
app.include_router(routes_credenciales.router)
app.include_router(routes_verificacion.router)
app.include_router(routes_documentos.router)
app.include_router(routes_auditoria.router)
app.include_router(routes_tramites.router)

ERROR_CONTRACTS = {
    ConsentimientoRequeridoError: (409, "CONSENT_REQUIRED"),
    IdentidadNoEncontradaError: (404, "IDENTITY_NOT_FOUND"),
    CredencialNoRegistradaError: (404, "CREDENTIAL_NOT_FOUND"),
    SesionNoEncontradaError: (404, "SESSION_NOT_FOUND"),
    SesionNoVigenteError: (409, "SESSION_NOT_ACTIVE"),
    RostroNoDetectadoError: (422, "FACE_NOT_DETECTED"),
    TramiteNoHabilitadoError: (409, "PROCEDURE_NOT_ENABLED"),
    DocumentoNoEncontradoError: (404, "DOCUMENT_NOT_FOUND"),
}


@app.exception_handler(NotaryVerifyError)
async def handle_domain_error(_: Request, exc: NotaryVerifyError):
    status_code, code = ERROR_CONTRACTS.get(type(exc), (400, "DOMAIN_ERROR"))
    return JSONResponse(status_code=status_code, content={"detail": {"code": code, "message": str(exc)}})


@app.exception_handler(ValueError)
async def handle_validation_error(_: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={"detail": {"code": "INPUT_INVALID", "message": str(exc)}})


@app.get("/", tags=["Estado"])
def estado():
    return {
        "sistema": "NotaryVerify",
        "estado": "operativo",
        "aviso": "Prototipo académico sin valor de identificación legal.",
    }
