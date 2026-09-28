from datetime import timedelta

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.models.db_models import SesionVerificacion, _now
from app.models.enums import EstadoSesion, ResultadoVerificacion as R, RolUsuario
from app.services.auth_service import AuthService
from app.services.verificacion_service import VerificacionService


def test_expired_sessions_are_materialized_and_history_is_filtered(db_session):
    admin = AuthService(db_session).create_user("Admin", "admin@example.test", "clave", RolUsuario.ADMINISTRADOR)
    operador = AuthService(db_session).create_user("Operador", "operator@example.test", "clave", RolUsuario.OPERADOR)
    expired = SesionVerificacion(id_identidad="identidad-a", id_responsable=operador.id, fecha_inicio=_now() - timedelta(minutes=11))
    approved = SesionVerificacion(
        id_identidad="identidad-b", id_responsable=operador.id, estado=EstadoSesion.COMPLETADA,
        resultado=R.IDENTIDAD_VERIFICADA, fecha_fin=_now(),
    )
    db_session.add_all([expired, approved])
    db_session.commit()

    assert VerificacionService(db_session).expirar_sesiones_vencidas() == 1
    assert db_session.get(SesionVerificacion, expired.id).estado == EstadoSesion.EXPIRADA

    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            login = client.post("/auth/login", json={"correo": admin.correo, "password": "clave"})
            headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
            response = client.get(f"/verificaciones?resultado={R.IDENTIDAD_VERIFICADA}&id_identidad=identidad-b", headers=headers)
            assert response.status_code == 200
            assert [session["id"] for session in response.json()] == [approved.id]
            assert response.json()[0]["id_responsable"] == operador.id
            assert "referencia_facial_path" not in response.json()[0]
    finally:
        app.dependency_overrides.clear()
