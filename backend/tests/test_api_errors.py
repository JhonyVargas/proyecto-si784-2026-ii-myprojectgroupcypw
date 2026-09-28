from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.models.enums import RolUsuario
from app.services.auth_service import AuthService


def test_domain_errors_have_stable_http_contract(db_session):
    AuthService(db_session).create_user("Admin", "admin@example.test", "clave", RolUsuario.ADMINISTRADOR)
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            login = client.post("/auth/login", json={"correo": "admin@example.test", "password": "clave"})
            headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
            credential = client.get("/credenciales/NO-EXISTE", headers=headers)
            assert credential.status_code == 404
            assert credential.json()["detail"]["code"] == "CREDENTIAL_NOT_FOUND"
            identity = client.get("/identidades/no-existe", headers=headers)
            assert identity.status_code == 404
            assert identity.json()["detail"]["code"] == "IDENTITY_NOT_FOUND"
    finally:
        app.dependency_overrides.clear()
