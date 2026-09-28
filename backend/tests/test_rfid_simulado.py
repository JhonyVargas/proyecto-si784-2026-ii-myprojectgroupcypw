import pytest
from fastapi.testclient import TestClient

import app.services.identidad_service as identidad_module
from app.models import schemas
from app.models.enums import EstadoCredencial, ResultadoVerificacion as R, TipoCredencial
from app.services.consentimiento_service import ConsentimientoService
from app.services.credencial_service import CredencialService
from app.services.errors import CredencialNoRegistradaError
from app.services.identidad_service import IdentidadService
from app.services.verificacion_service import VerificacionService
from app.core.database import get_db
from app.main import app
from app.services.auth_service import AuthService
from app.models.enums import RolUsuario


def _identity(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(identidad_module, "REFERENCIAS_DIR", tmp_path)
    ConsentimientoService(db_session).otorgar(schemas.ConsentimientoCrear(id_participante="rfid-voluntario"))
    return IdentidadService(db_session).registrar(
        schemas.IdentidadCrear(nombre_ficticio="PERSONA-RFID", documento_ficticio="RFID-001", id_participante="rfid-voluntario", confirmo_dato_ficticio=True),
        b"referencia-sintetica",
    )


def test_simulated_rfid_uid_reads_only_its_associated_credential(db_session, tmp_path, monkeypatch):
    identity = _identity(db_session, tmp_path, monkeypatch)
    service = CredencialService(db_session)
    credential = service.emitir(schemas.CredencialCrear(id_identidad=identity.id, tipo=TipoCredencial.RFID, uid_rfid="04A1B2C3"))

    read = service.leer_rfid("04A1B2C3")
    assert read.id == credential.id
    assert read.id_identidad == identity.id
    assert read.tipo == TipoCredencial.RFID

    # Leer solo selecciona la credencial; el motor multicapa aún rechaza sin rostro/vida.
    session = VerificacionService(db_session).iniciar_sesion(read.codigo, None)
    assert session.resultado is None


def test_simulated_rfid_reuses_revocation_and_missing_behavior(db_session, tmp_path, monkeypatch):
    identity = _identity(db_session, tmp_path, monkeypatch)
    service = CredencialService(db_session)
    credential = service.emitir(schemas.CredencialCrear(id_identidad=identity.id, tipo=TipoCredencial.RFID, uid_rfid="A0B1C2D3"))
    service.revocar(credential.id)

    assert service.leer_rfid("A0B1C2D3").estado == EstadoCredencial.REVOCADA
    rejected = VerificacionService(db_session).iniciar_sesion("A0B1C2D3", None)
    assert rejected.resultado == R.CREDENCIAL_REVOCADA
    with pytest.raises(CredencialNoRegistradaError):
        service.leer_rfid("DEADBEEF")


def test_rfid_api_uses_same_authenticated_credential_contract(db_session, tmp_path, monkeypatch):
    identity = _identity(db_session, tmp_path, monkeypatch)
    credential = CredencialService(db_session).emitir(
        schemas.CredencialCrear(id_identidad=identity.id, tipo=TipoCredencial.RFID, uid_rfid="1122AABB")
    )
    AuthService(db_session).create_user("Admin", "admin@example.test", "clave", RolUsuario.ADMINISTRADOR)
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            login = client.post("/auth/login", json={"correo": "admin@example.test", "password": "clave"})
            headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
            response = client.get("/credenciales/rfid/1122AABB", headers=headers)
            assert response.status_code == 200
            assert response.json()["id"] == credential.id
    finally:
        app.dependency_overrides.clear()


@pytest.mark.parametrize("uid", ["04-a1", "04a1", "", "G4A1"])
def test_simulated_rfid_rejects_noncanonical_uids(db_session, uid):
    with pytest.raises(ValueError):
        CredencialService(db_session).leer_rfid(uid)
