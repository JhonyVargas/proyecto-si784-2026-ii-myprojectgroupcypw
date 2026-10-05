"""Pruebas de integridad documental mediante SHA-256 (RN-08)."""

import app.services.documento_service as documento_service_module
from app.services.documento_service import DocumentoService


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
