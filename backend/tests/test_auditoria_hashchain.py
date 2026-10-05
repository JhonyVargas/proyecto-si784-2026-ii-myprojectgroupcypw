"""Pruebas de la bitácora de auditoría con encadenamiento criptográfico (RN-07)."""

from app.models.db_models import EventoAuditoria, SesionVerificacion
from app.services.auditoria_service import AuditoriaService, GENESIS_HASH


def test_primer_evento_se_enlaza_con_el_hash_genesis(db_session):
    servicio = AuditoriaService(db_session)
    evento = servicio.registrar_evento("sesion-1", "SESION_INICIADA", {"paso": 1})

    assert evento.hash_evento_anterior == GENESIS_HASH
    assert evento.secuencia == 1


def test_cadena_valida_sin_alteraciones(db_session):
    servicio = AuditoriaService(db_session)
    servicio.registrar_evento("sesion-1", "SESION_INICIADA", {"paso": 1})
    servicio.registrar_evento("sesion-1", "ROSTRO_EVALUADO", {"coincide": True, "confianza": 0.8})
    servicio.registrar_evento(
        "sesion-1", "SESION_FINALIZADA", {"resultado": "IDENTIDAD_VERIFICADA"}
    )

    verificacion = servicio.verificar_cadena()

    assert verificacion.valida is True
    assert verificacion.total_eventos == 3
    assert verificacion.primer_evento_alterado is None


def test_detecta_alteracion_deliberada_de_un_evento(db_session):
    """RN-07: alterar un evento ya registrado debe romper la cadena a partir de él."""

    servicio = AuditoriaService(db_session)
    servicio.registrar_evento("sesion-1", "SESION_INICIADA", {"paso": 1})
    evento_2 = servicio.registrar_evento("sesion-1", "ROSTRO_EVALUADO", {"coincide": True})
    servicio.registrar_evento(
        "sesion-1", "SESION_FINALIZADA", {"resultado": "IDENTIDAD_VERIFICADA"}
    )

    # Alteración maliciosa directa en la base de datos, sin pasar por
    # `registrar_evento` (el único método autorizado para escribir eventos).
    evento_en_db = db_session.get(EventoAuditoria, evento_2.id)
    evento_en_db.detalle = '{"coincide": false}'
    db_session.commit()

    verificacion = servicio.verificar_cadena()

    assert verificacion.valida is False
    assert verificacion.primer_evento_alterado == evento_2.id


def test_listar_eventos_filtra_por_sesion(db_session):
    servicio = AuditoriaService(db_session)
    servicio.registrar_evento("sesion-A", "SESION_INICIADA", {})
    servicio.registrar_evento("sesion-B", "SESION_INICIADA", {})

    eventos_a = servicio.listar_eventos("sesion-A")

    assert len(eventos_a) == 1
    assert eventos_a[0].id_sesion == "sesion-A"


def test_reconstruye_sesion_con_payload_minimo_sin_credencial(db_session):
    sesion = SesionVerificacion()
    db_session.add(sesion)
    db_session.commit()
    servicio = AuditoriaService(db_session)
    servicio.registrar_evento(
        sesion.id,
        "SESION_INICIADA",
        {"codigo_credencial": "SECRETO-NO-EXPOSICION", "actor": "operador-1"},
    )
    servicio.registrar_evento(
        sesion.id,
        "SESION_FINALIZADA",
        {"resultado": "IDENTIDAD_VERIFICADA", "actor": "operador-1"},
    )

    reconstruccion = servicio.reconstruir_sesion(sesion.id)

    assert [evento.tipo_evento for evento in reconstruccion.eventos] == [
        "SESION_INICIADA", "SESION_FINALIZADA"
    ]
    assert reconstruccion.eventos[0].actor == "operador-1"
    assert reconstruccion.eventos[0].entidad == "SESION_VERIFICACION"
    assert reconstruccion.eventos[0].payload_minimo == {}
    assert reconstruccion.eventos[1].payload_minimo == {"resultado": "IDENTIDAD_VERIFICADA"}
