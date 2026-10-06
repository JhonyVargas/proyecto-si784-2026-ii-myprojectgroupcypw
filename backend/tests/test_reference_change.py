import app.services.identidad_service as identidad_module
from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.models import schemas
from app.models.enums import RolUsuario
from app.services.auditoria_service import AuditoriaService
from app.services.auth_service import AuthService
from app.services.consentimiento_service import ConsentimientoService
from app.services.identidad_service import IdentidadService


def _token(client, correo):
    response = client.post("/auth/login", json={"correo": correo, "password": "clave"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_operator_requests_and_only_admin_approves_reference_change(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(identidad_module, "REFERENCIAS_DIR", tmp_path / "active")
    monkeypatch.setattr(identidad_module, "REFERENCIAS_PENDIENTES_DIR", tmp_path / "pending")
    identidad_module.REFERENCIAS_DIR.mkdir()
    identidad_module.REFERENCIAS_PENDIENTES_DIR.mkdir()
    ConsentimientoService(db_session).otorgar(schemas.ConsentimientoCrear(id_participante="voluntario-ref"))
    identity = IdentidadService(db_session).registrar(
        schemas.IdentidadCrear(nombre_ficticio="PERSONA-REF", documento_ficticio="REF-001", id_participante="voluntario-ref", confirmo_dato_ficticio=True), b"anterior"
    )
    AuthService(db_session).create_user("Operador", "operator@example.test", "clave", RolUsuario.OPERADOR)
    AuthService(db_session).create_user("Admin", "admin@example.test", "clave", RolUsuario.ADMINISTRADOR)
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            operator = _token(client, "operator@example.test")
            admin = _token(client, "admin@example.test")
            request = client.post(f"/identidades/{identity.id}/referencia/solicitudes", headers=operator, data={"motivo": "Imagen de referencia renovada"}, files={"imagen_referencia": ("nueva.jpg", b"\xff\xd8\xffnueva", "image/jpeg")})
            assert request.status_code == 201
            request_id = request.json()["id"]
            assert client.post(f"/identidades/referencia/solicitudes/{request_id}/decision", headers=operator, json={"aprobar": True, "motivo_decision": "no autorizado"}).status_code == 403
            approved = client.post(f"/identidades/referencia/solicitudes/{request_id}/decision", headers=admin, json={"aprobar": True, "motivo_decision": "Consentimiento y calidad verificados"})
            assert approved.status_code == 200
            assert approved.json()["estado"] == "APROBADA"
    finally:
        app.dependency_overrides.clear()
    assert (tmp_path / "active" / f"{identity.id}.jpg").read_bytes() == b"\xff\xd8\xffnueva"
    details = [event.detalle for event in AuditoriaService(db_session).listar_eventos()]
    assert any("CAMBIO_REFERENCIA_DECIDIDO" in event.tipo_evento for event in AuditoriaService(db_session).listar_eventos())
    assert all("referencia_pendiente_path" not in detail and "nueva.jpg" not in detail for detail in details)


def test_rejected_request_deletes_pending_biometric_reference(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(identidad_module, "REFERENCIAS_DIR", tmp_path / "active")
    monkeypatch.setattr(identidad_module, "REFERENCIAS_PENDIENTES_DIR", tmp_path / "pending")
    identidad_module.REFERENCIAS_DIR.mkdir()
    identidad_module.REFERENCIAS_PENDIENTES_DIR.mkdir()
    ConsentimientoService(db_session).otorgar(schemas.ConsentimientoCrear(id_participante="voluntario-reject"))
    identity = IdentidadService(db_session).registrar(schemas.IdentidadCrear(nombre_ficticio="PERSONA-RECHAZO", documento_ficticio="REF-002", id_participante="voluntario-reject", confirmo_dato_ficticio=True), b"anterior")
    request = IdentidadService(db_session).solicitar_cambio_referencia(identity.id, "actor", "Nueva captura borrosa", b"pendiente")
    pending = request.referencia_pendiente_path
    result = IdentidadService(db_session).decidir_cambio_referencia(request.id, "admin", False, "Calidad insuficiente")
    assert result.estado == "RECHAZADA"
    assert not __import__("pathlib").Path(pending).exists()
