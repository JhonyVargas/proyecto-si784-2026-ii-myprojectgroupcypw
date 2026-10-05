from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.models.db_models import SesionVerificacion
from app.services.auditoria_service import AuditoriaService
from app.models.enums import RolUsuario
from app.services.auth_service import AuthService


def _login(client, correo, password):
    response = client.post("/auth/login", json={"correo": correo, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_role_matrix_restricts_administration_and_assigns_operator(db_session):
    operador = AuthService(db_session).create_user("Operador", "operator@example.test", "clave", RolUsuario.OPERADOR)
    AuthService(db_session).create_user("Admin", "admin@example.test", "clave", RolUsuario.ADMINISTRADOR)
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            operator_headers = _login(client, "operator@example.test", "clave")
            admin_headers = _login(client, "admin@example.test", "clave")

            assert client.get("/identidades", headers=operator_headers).status_code == 403
            assert client.get("/auditoria/eventos", headers=operator_headers).status_code == 403
            assert client.get("/identidades", headers=admin_headers).status_code == 200
            assert client.get("/auditoria/eventos", headers=admin_headers).status_code == 200

            audited_session = SesionVerificacion()
            db_session.add(audited_session)
            db_session.commit()
            AuditoriaService(db_session).registrar_evento(
                audited_session.id, "SESION_INICIADA", {}
            )
            assert client.get(
                f"/auditoria/sesiones/{audited_session.id}/reconstruccion",
                headers=operator_headers,
            ).status_code == 403
            assert client.get(
                f"/auditoria/sesiones/{audited_session.id}/reconstruccion",
                headers=admin_headers,
            ).status_code == 200

            # El valor id_responsable enviado por el cliente no se acepta como autoridad.
            started = client.post(
                "/verificaciones",
                headers=operator_headers,
                json={"codigo_credencial": "NO-EXISTE", "id_responsable": "suplantado"},
            )
            assert started.status_code == 201
            session = db_session.get(SesionVerificacion, started.json()["id"])
            assert session.id_responsable == operador.id
    finally:
        app.dependency_overrides.clear()
