"""Pruebas de integridad documental mediante SHA-256 (RN-08)."""

import pytest

import app.services.documento_service as documento_service_module
from app.models.db_models import SesionVerificacion
from app.services.documento_service import DocumentoService
from app.services.errors import SesionNoEncontradaError


@pytest.fixture(autouse=True)
def sesiones(db_session):
    db_session.add_all([SesionVerificacion(id="sesion-1"), SesionVerificacion(id="sesion-secreta")])
    db_session.commit()


def test_documento_integro_con_el_mismo_contenido(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(documento_service_module, "DOCUMENTOS_DIR", tmp_path)

    servicio = DocumentoService(db_session)
    documento = servicio.generar_documento("sesion-1", "Contenido de prueba NotaryVerify")

    resultado = servicio.verificar_integridad(
        documento.id, "Contenido de prueba NotaryVerify".encode("utf-8")
    )

    assert resultado.integro is True
    assert resultado.hash_calculado == resultado.hash_esperado


def test_documento_no_integro_tras_una_modificacion(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(documento_service_module, "DOCUMENTOS_DIR", tmp_path)

    servicio = DocumentoService(db_session)
    documento = servicio.generar_documento("sesion-1", "Contenido original")

    resultado = servicio.verificar_integridad(documento.id, "Contenido alterado".encode("utf-8"))

    assert resultado.integro is False
    assert resultado.hash_calculado != resultado.hash_esperado


def test_qr_de_verificacion_no_incluye_datos_personales(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(documento_service_module, "DOCUMENTOS_DIR", tmp_path)

    servicio = DocumentoService(db_session)
    documento = servicio.generar_documento("sesion-1", "Contenido de prueba")

    assert documento.qr_verificacion == f"NOTARYVERIFY-DOC-{documento.id}"
    assert "sesion-1" not in documento.qr_verificacion


def test_consulta_qr_publica_no_expone_sesion_hash_ni_contenido(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(documento_service_module, "DOCUMENTOS_DIR", tmp_path)
    documento = DocumentoService(db_session).generar_documento("sesion-secreta", "Contenido de prueba")
    consulta = DocumentoService(db_session).consultar_qr(documento.qr_verificacion)
    assert consulta.estado == "INTEGRO"
    assert "sesion" not in consulta.model_dump_json()
    assert "hash" not in consulta.model_dump_json().lower()


def test_consulta_qr_informa_integridad_invalida(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(documento_service_module, "DOCUMENTOS_DIR", tmp_path)
    documento = DocumentoService(db_session).generar_documento("sesion-1", "original")
    open(documento.contenido_path, "wb").write(b"alterado")
    assert DocumentoService(db_session).consultar_qr(documento.qr_verificacion).estado == "INTEGRIDAD_NO_VERIFICADA"


def test_documento_requiere_sesion_existente_y_no_usa_ruta_del_cliente(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(documento_service_module, "DOCUMENTOS_DIR", tmp_path)

    with pytest.raises(SesionNoEncontradaError):
        DocumentoService(db_session).generar_documento("../../fuera", "contenido")

    assert list(tmp_path.iterdir()) == []


def test_documentos_de_una_misma_sesion_no_se_sobrescriben(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(documento_service_module, "DOCUMENTOS_DIR", tmp_path)
    servicio = DocumentoService(db_session)

    primero = servicio.generar_documento("sesion-1", "primero")
    segundo = servicio.generar_documento("sesion-1", "segundo")

    assert primero.contenido_path != segundo.contenido_path
    assert servicio.consultar_qr(primero.qr_verificacion).estado == "INTEGRO"
    assert servicio.consultar_qr(segundo.qr_verificacion).estado == "INTEGRO"
