import pytest
from fastapi.testclient import TestClient

import app.services.documento_service as documento_service_module
from app.core.database import get_db
from app.main import app
from app.models.db_models import SesionVerificacion
from app.models.enums import ResultadoVerificacion as R, RolUsuario
from app.services.auditoria_service import AuditoriaService
from app.services.auth_service import AuthService
from app.services.documento_service import DocumentoService
from app.services.errors import DocumentoIntegridadInvalidaError, TramiteNoHabilitadoError
from app.services.sid_sunarp_service import SidSunarpSimuladoService


def _sesion_y_documento(db_session, tmp_path, monkeypatch, resultado=R.IDENTIDAD_VERIFICADA):
    monkeypatch.setattr(documento_service_module, "DOCUMENTOS_DIR", tmp_path)
    sesion = SesionVerificacion(resultado=resultado)
    db_session.add(sesion)
    db_session.commit()
    documento = DocumentoService(db_session).generar_documento(sesion.id, "Documento sintético")
    return sesion, documento


@pytest.mark.parametrize("escenario,estado", [
    ("DISPONIBLE", "ENVIADO"), ("RECHAZADO", "RECHAZADO"),
    ("SERVICIO_NO_DISPONIBLE", "ERROR_SERVICIO"), ("TIEMPO_AGOTADO", "TIEMPO_AGOTADO"),
    ("RESPUESTA_INVALIDA", "RESPUESTA_INVALIDA"), ("ERROR_INTERNO", "ERROR_INTERNO"),
])
def test_escenarios_sid_son_deterministas_y_auditados(db_session, tmp_path, monkeypatch, escenario, estado):
    sesion, documento = _sesion_y_documento(db_session, tmp_path, monkeypatch)
    servicio = SidSunarpSimuladoService(db_session)
    tramite = servicio.enviar_tramite(sesion.id, documento.id, escenario)
    evidencia = servicio.obtener_evidencia(tramite.id)

    assert tramite.estado == estado
    assert evidencia.id_sesion == sesion.id
    assert evidencia.id_documento == documento.id
    assert evidencia.integridad_documento == "INTEGRO"
    eventos = [e.tipo_evento for e in AuditoriaService(db_session).listar_eventos(sesion.id)]
    assert eventos[-2:] == ["EVIDENCIA_TRAMITE_ASOCIADA", "TRAMITE_SIMULADO_EVALUADO"]


def test_sesion_no_aprobada_no_invoca_simulador(db_session, tmp_path, monkeypatch):
    sesion, documento = _sesion_y_documento(
        db_session, tmp_path, monkeypatch, R.PRUEBA_DE_VIDA_FALLIDA
    )
    with pytest.raises(TramiteNoHabilitadoError):
        SidSunarpSimuladoService(db_session).enviar_tramite(sesion.id, documento.id)
    assert not AuditoriaService(db_session).listar_eventos(sesion.id)


def test_documento_alterado_bloquea_tramite_y_no_deja_auditoria(db_session, tmp_path, monkeypatch):
    sesion, documento = _sesion_y_documento(db_session, tmp_path, monkeypatch)
    open(documento.contenido_path, "wb").write(b"contenido alterado")

    with pytest.raises(DocumentoIntegridadInvalidaError):
        SidSunarpSimuladoService(db_session).enviar_tramite(sesion.id, documento.id)

    assert not AuditoriaService(db_session).listar_eventos(sesion.id)


def test_evidencia_minima_no_expone_contenido_ni_hash(db_session, tmp_path, monkeypatch):
    sesion, documento = _sesion_y_documento(db_session, tmp_path, monkeypatch)
    servicio = SidSunarpSimuladoService(db_session)
    tramite = servicio.enviar_tramite(sesion.id, documento.id)

    evidencia = servicio.obtener_evidencia(tramite.id).model_dump_json().lower()

    assert "documento sintético" not in evidencia
    assert "hash" not in evidencia
    assert "contenido_path" not in evidencia


def test_evidencia_requiere_auditor_o_administrador(db_session, tmp_path, monkeypatch):
    sesion, documento = _sesion_y_documento(db_session, tmp_path, monkeypatch)
    tramite = SidSunarpSimuladoService(db_session).enviar_tramite(sesion.id, documento.id)
    AuthService(db_session).create_user("Operador", "operator@example.test", "clave", RolUsuario.OPERADOR)
    AuthService(db_session).create_user("Auditor", "auditor@example.test", "clave", RolUsuario.AUDITOR)
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            assert client.get(f"/tramites/{tramite.id}/evidencia").status_code == 401
            token_operador = client.post(
                "/auth/login", json={"correo": "operator@example.test", "password": "clave"}
            ).json()["access_token"]
            assert client.get(
                f"/tramites/{tramite.id}/evidencia",
                headers={"Authorization": f"Bearer {token_operador}"},
            ).status_code == 403
            token_auditor = client.post(
                "/auth/login", json={"correo": "auditor@example.test", "password": "clave"}
            ).json()["access_token"]
            response = client.get(
                f"/tramites/{tramite.id}/evidencia",
                headers={"Authorization": f"Bearer {token_auditor}"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["id_documento"] == documento.id
    assert "hash" not in response.text.lower()


def _cliente_operador(client, db_session):
    AuthService(db_session).create_user("Operador UI", "operador.ui@example.test", "clave", RolUsuario.OPERADOR)
    token = client.post(
        "/auth/login", json={"correo": "operador.ui@example.test", "password": "clave"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_flujo_ui_fallo_externo_no_altera_sesion_y_permite_reintento(db_session, tmp_path, monkeypatch):
    """Recorrido HTTP que usa la estación (#20): documento, fallo externo y reintento."""
    monkeypatch.setattr(documento_service_module, "DOCUMENTOS_DIR", tmp_path)
    sesion = SesionVerificacion(resultado=R.IDENTIDAD_VERIFICADA)
    db_session.add(sesion)
    db_session.commit()
    estado_inicial = sesion.estado
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            headers = _cliente_operador(client, db_session)
            documento = client.post(
                "/documentos", headers=headers,
                params={"id_sesion": sesion.id}, data={"contenido": "Minuta ficticia"},
            ).json()
            fallido = client.post("/tramites", headers=headers, params={
                "id_sesion": sesion.id, "id_documento": documento["id"],
                "escenario": "SERVICIO_NO_DISPONIBLE",
            })
            reintento = client.post("/tramites", headers=headers, params={
                "id_sesion": sesion.id, "id_documento": documento["id"], "escenario": "DISPONIBLE",
            })
    finally:
        app.dependency_overrides.clear()

    assert fallido.status_code == 201
    assert fallido.json()["estado"] == "ERROR_SERVICIO"
    assert reintento.status_code == 201
    assert reintento.json()["estado"] == "ENVIADO"
    assert reintento.json()["id"] != fallido.json()["id"]
    db_session.refresh(sesion)
    assert sesion.resultado == R.IDENTIDAD_VERIFICADA
    assert sesion.estado == estado_inicial


def test_flujo_ui_sesion_rechazada_recibe_codigo_sin_detalle_interno(db_session, tmp_path, monkeypatch):
    sesion, documento = _sesion_y_documento(
        db_session, tmp_path, monkeypatch, R.ROSTRO_NO_COINCIDENTE
    )
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            headers = _cliente_operador(client, db_session)
            response = client.post("/tramites", headers=headers, params={
                "id_sesion": sesion.id, "id_documento": documento.id,
            })
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "PROCEDURE_NOT_ENABLED"
    assert documento.contenido_path not in response.text
    assert documento.hash_sha256 not in response.text
