"""Evidencia reproducible de los cuatro escenarios críticos del MVP (#10).

Los adaptadores biométricos se simulan explícitamente: esta prueba verifica el
orquestador, API de dominio, persistencia y reglas sin cámara, modelos ni red.
"""

from app.models import schemas
from app.models.enums import EstadoSesion, ResultadoVerificacion as R
from app.services.consentimiento_service import ConsentimientoService
from app.services.credencial_service import CredencialService
from app.services.identidad_service import IdentidadService
from app.services.verificacion_service import VerificacionService
import app.services.identidad_service as identidad_module


def _credential(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(identidad_module, "REFERENCIAS_DIR", tmp_path)
    ConsentimientoService(db_session).otorgar(schemas.ConsentimientoCrear(id_participante="mvp-voluntario"))
    identity = IdentidadService(db_session).registrar(
        schemas.IdentidadCrear(nombre_ficticio="PERSONA-MVP", documento_ficticio="MVP-001", id_participante="mvp-voluntario", confirmo_dato_ficticio=True),
        b"referencia-sintetica",
    )
    return CredencialService(db_session).emitir(schemas.CredencialCrear(id_identidad=identity.id))


def test_mvp_valid_credential_face_and_liveness_are_approved(db_session, tmp_path, monkeypatch):
    credential = _credential(db_session, tmp_path, monkeypatch)
    service = VerificacionService(db_session)
    monkeypatch.setattr(service.biometria, "comparar_rostro", lambda *_: (True, 0.99))
    monkeypatch.setattr(service.liveness, "validar_accion", lambda *_: (True, {"metrica": "simulada"}))
    session = service.iniciar_sesion(credential.codigo, None)
    service.registrar_captura_facial(session.id, b"captura")
    result = service.registrar_prueba_vida(session.id, "PARPADEO", b"captura")
    assert (result.estado, result.resultado) == (EstadoSesion.COMPLETADA, R.IDENTIDAD_VERIFICADA)


def test_mvp_non_matching_face_is_rejected(db_session, tmp_path, monkeypatch):
    credential = _credential(db_session, tmp_path, monkeypatch)
    service = VerificacionService(db_session)
    monkeypatch.setattr(service.biometria, "comparar_rostro", lambda *_: (False, 0.1))
    session = service.iniciar_sesion(credential.codigo, None)
    assert service.registrar_captura_facial(session.id, b"captura").resultado == R.ROSTRO_NO_COINCIDENTE


def test_mvp_failed_liveness_is_rejected(db_session, tmp_path, monkeypatch):
    credential = _credential(db_session, tmp_path, monkeypatch)
    service = VerificacionService(db_session)
    monkeypatch.setattr(service.biometria, "comparar_rostro", lambda *_: (True, 0.99))
    monkeypatch.setattr(service.liveness, "validar_accion", lambda *_: (False, {"metrica": "simulada"}))
    session = service.iniciar_sesion(credential.codigo, None)
    service.registrar_captura_facial(session.id, b"captura")
    assert service.registrar_prueba_vida(session.id, "PARPADEO", b"captura").resultado == R.PRUEBA_DE_VIDA_FALLIDA


def test_mvp_unknown_credential_is_rejected(db_session):
    session = VerificacionService(db_session).iniciar_sesion("NV-MVP-NO-EXISTE", None)
    assert (session.estado, session.resultado) == (EstadoSesion.COMPLETADA, R.CREDENCIAL_NO_REGISTRADA)
