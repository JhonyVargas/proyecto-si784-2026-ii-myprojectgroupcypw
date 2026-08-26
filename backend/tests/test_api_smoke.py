"""Prueba de humo: la aplicación FastAPI arranca y expone su documentación."""

from fastapi.testclient import TestClient

from app.main import app


def test_endpoint_estado_responde_ok():
    with TestClient(app) as cliente:
        respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json()["sistema"] == "NotaryVerify"


def test_openapi_schema_se_genera_correctamente():
    with TestClient(app) as cliente:
        respuesta = cliente.get("/openapi.json")
    assert respuesta.status_code == 200
