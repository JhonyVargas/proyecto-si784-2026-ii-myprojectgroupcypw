"""Pruebas del orquestador de verificación multicapa (CU-03)."""

import app.services.identidad_service as identidad_service_module
from app.models import schemas
from app.models.enums import EstadoSesion
from app.models.enums import ResultadoVerificacion as R
from app.services.auditoria_service import AuditoriaService
from app.services.consentimiento_service import ConsentimientoService
from app.services.credencial_service import CredencialService
from app.services.identidad_service import IdentidadService
from app.services.verificacion_service import VerificacionService


def test_verificacion_con_credencial_no_registrada(db_session):
    servicio = VerificacionService(db_session)
    sesion = servicio.iniciar_sesion("NV-INEXISTENTE", id_responsable=None)

    assert sesion.resultado == R.CREDENCIAL_NO_REGISTRADA
    assert sesion.estado == EstadoSesion.COMPLETADA


def _crear_identidad_y_credencial(db_session, tmp_path, monkeypatch, id_participante):
    monkeypatch.setattr(identidad_service_module, "REFERENCIAS_DIR", tmp_path)

    ConsentimientoService(db_session).otorgar(
        schemas.ConsentimientoCrear(id_participante=id_participante)
    )
    identidad = IdentidadService(db_session).registrar(
        schemas.IdentidadCrear(
            nombre_ficticio="PERSONA-DE-PRUEBA",
            documento_ficticio=f"X{id_participante}",
            id_participante=id_participante,
            confirmo_dato_ficticio=True,
        ),
        b"contenido-imagen-simulada",
    )
    credencial_service = CredencialService(db_session)
    credencial = credencial_service.emitir(schemas.CredencialCrear(id_identidad=identidad.id))
    return identidad, credencial, credencial_service


def test_verificacion_con_credencial_revocada_rn04(db_session, tmp_path, monkeypatch):
    _identidad, credencial, credencial_service = _crear_identidad_y_credencial(
        db_session, tmp_path, monkeypatch, "voluntario-revocado"
    )
    credencial_service.revocar(credencial.id)

    servicio = VerificacionService(db_session)
    sesion = servicio.iniciar_sesion(credencial.codigo, id_responsable=None)

    assert sesion.resultado == R.CREDENCIAL_REVOCADA


def test_bitacora_registra_los_eventos_de_la_sesion(db_session):
    servicio = VerificacionService(db_session)
    sesion = servicio.iniciar_sesion("NV-OTRO-INEXISTENTE", id_responsable=None)

    eventos = AuditoriaService(db_session).listar_eventos(sesion.id)
    tipos = [e.tipo_evento for e in eventos]

    assert "SESION_INICIADA" in tipos
    assert "SESION_FINALIZADA" in tipos


def test_tres_intentos_fallidos_consecutivos_bloquean_la_identidad_rn05(
    db_session, tmp_path, monkeypatch
):
    identidad, credencial, credencial_service = _crear_identidad_y_credencial(
        db_session, tmp_path, monkeypatch, "voluntario-bloqueo"
    )
    credencial_service.revocar(credencial.id)
    servicio = VerificacionService(db_session)

    for _ in range(3):
        servicio.iniciar_sesion(credencial.codigo, id_responsable=None)

    identidad_actualizada = IdentidadService(db_session).consultar(identidad.id)
    assert identidad_actualizada.estado == "BLOQUEADA"
