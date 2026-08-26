"""Pruebas del Simulador de Identidad y de credenciales (RN-02, RN-03, RN-04)."""

import pytest

import app.services.identidad_service as identidad_service_module
from app.models import schemas
from app.services.consentimiento_service import ConsentimientoService
from app.services.credencial_service import CredencialService
from app.services.errors import ConsentimientoRequeridoError
from app.services.identidad_service import IdentidadService


def _crear_identidad_de_prueba(db_session, tmp_path, monkeypatch, id_participante="voluntario-1"):
    monkeypatch.setattr(identidad_service_module, "REFERENCIAS_DIR", tmp_path)

    ConsentimientoService(db_session).otorgar(
        schemas.ConsentimientoCrear(id_participante=id_participante)
    )
    datos = schemas.IdentidadCrear(
        nombre_ficticio="PERSONA-001",
        documento_ficticio="X0000001",
        id_participante=id_participante,
        confirmo_dato_ficticio=True,
    )
    return IdentidadService(db_session).registrar(datos, b"contenido-imagen-simulada")


def test_no_se_puede_registrar_identidad_sin_consentimiento_previo(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(identidad_service_module, "REFERENCIAS_DIR", tmp_path)

    datos = schemas.IdentidadCrear(
        nombre_ficticio="PERSONA-002",
        documento_ficticio="X0000002",
        id_participante="sin-consentimiento",
        confirmo_dato_ficticio=True,
    )

    with pytest.raises(ConsentimientoRequeridoError):
        IdentidadService(db_session).registrar(datos, b"contenido-imagen-simulada")


def test_no_se_puede_registrar_identidad_sin_confirmar_dato_ficticio(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(identidad_service_module, "REFERENCIAS_DIR", tmp_path)

    ConsentimientoService(db_session).otorgar(
        schemas.ConsentimientoCrear(id_participante="voluntario-x")
    )
    datos = schemas.IdentidadCrear(
        nombre_ficticio="PERSONA-003",
        documento_ficticio="X0000003",
        id_participante="voluntario-x",
        confirmo_dato_ficticio=False,
    )

    with pytest.raises(ValueError):
        IdentidadService(db_session).registrar(datos, b"contenido-imagen-simulada")


def test_credencial_revocada_es_detectada_al_leerla(db_session, tmp_path, monkeypatch):
    identidad = _crear_identidad_de_prueba(db_session, tmp_path, monkeypatch)
    servicio = CredencialService(db_session)
    credencial = servicio.emitir(schemas.CredencialCrear(id_identidad=identidad.id))

    servicio.revocar(credencial.id)
    credencial_leida = servicio.leer(credencial.codigo)

    assert credencial_leida.estado == "REVOCADA"


def test_codigo_de_credencial_es_unico_por_emision(db_session, tmp_path, monkeypatch):
    identidad = _crear_identidad_de_prueba(db_session, tmp_path, monkeypatch)
    servicio = CredencialService(db_session)

    credencial_1 = servicio.emitir(schemas.CredencialCrear(id_identidad=identidad.id))
    credencial_2 = servicio.emitir(schemas.CredencialCrear(id_identidad=identidad.id))

    assert credencial_1.codigo != credencial_2.codigo
