from datetime import timedelta

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.models.db_models import _now
from app.models.enums import RolUsuario
from app.services.auth_service import AuthService, verify_password


def test_password_is_salted_and_never_stored_in_plaintext(db_session):
    user = AuthService(db_session).create_user(
        "Operador sintético", "operator@example.test", "clave-de-prueba", RolUsuario.OPERADOR
    )

    assert user.password_hash != "clave-de-prueba"
    assert user.password_hash.startswith("scrypt$")
    assert verify_password("clave-de-prueba", user.password_hash)
    assert not verify_password("otra-clave", user.password_hash)


def test_login_logout_and_protected_current_user(db_session):
    AuthService(db_session).create_user(
        "Operador sintético", "operator@example.test", "clave-de-prueba", RolUsuario.OPERADOR
    )
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            unauthenticated = client.get("/auth/me")
            assert unauthenticated.status_code == 401
            assert unauthenticated.json()["detail"]["code"] == "AUTHENTICATION_REQUIRED"

            invalid = client.post("/auth/login", json={"correo": "operator@example.test", "password": "incorrecta"})
            assert invalid.status_code == 401
            assert invalid.json()["detail"]["code"] == "AUTHENTICATION_REQUIRED"

            login = client.post("/auth/login", json={"correo": "operator@example.test", "password": "clave-de-prueba"})
            assert login.status_code == 200
            payload = login.json()
            assert payload["access_token"]
            assert payload["usuario"]["rol"] == RolUsuario.OPERADOR
            token = payload["access_token"]

            me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
            assert me.status_code == 200
            assert me.json()["correo"] == "operator@example.test"

            logout = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
            assert logout.status_code == 204
            assert client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
    finally:
        app.dependency_overrides.clear()


def test_expired_token_is_rejected(db_session):
    user = AuthService(db_session).create_user(
        "Administrador sintético", "admin@example.test", "clave-de-prueba", RolUsuario.ADMINISTRADOR
    )
    token, session, _ = AuthService(db_session).login(user.correo, "clave-de-prueba")
    session.fecha_expiracion = _now() - timedelta(seconds=1)
    db_session.commit()

    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "AUTHENTICATION_REQUIRED"
    finally:
        app.dependency_overrides.clear()
