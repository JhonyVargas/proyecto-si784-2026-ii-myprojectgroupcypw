"""Pruebas offline del desafío temporal de vida experimental (#14).

Las fotografías impresas y en pantalla se representan como capturas estáticas
que no realizan la acción sorteada. No se usan personas, cámara ni vídeo.
"""

from types import SimpleNamespace

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

import app.services.identidad_service as identidad_service_module
import app.services.liveness_service as liveness_service_module
import app.services.verificacion_service as verificacion_service_module
from app.models import schemas
from app.models.db_models import Credencial
from app.models.enums import AccionPruebaVida, EstadoSesion, RolUsuario
from app.models.enums import ResultadoVerificacion as R
from app.core.database import get_db
from app.main import app
from app.services.auditoria_service import AuditoriaService
from app.services.auth_service import AuthService
from app.services.biometria_service import BiometriaService
from app.services.consentimiento_service import ConsentimientoService
from app.services.credencial_service import CredencialService
from app.services.errors import DesafioPruebaVidaAgotadoError, RostroMultipleDetectadoError
from app.services.identidad_service import IdentidadService
from app.services.liveness_service import LivenessService
from app.services.verificacion_service import VerificacionService


def _crear_sesion_con_rostro_aprobado(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(identidad_service_module, "REFERENCIAS_DIR", tmp_path)
    ConsentimientoService(db_session).otorgar(
        schemas.ConsentimientoCrear(id_participante="voluntario-liveness-sintetico")
    )
    identidad = IdentidadService(db_session).registrar(
        schemas.IdentidadCrear(
            nombre_ficticio="PERSONA-LIVENESS",
            documento_ficticio="LIVENESS-001",
            id_participante="voluntario-liveness-sintetico",
            confirmo_dato_ficticio=True,
        ),
        b"referencia-sintetica",
    )
    credencial = CredencialService(db_session).emitir(
        schemas.CredencialCrear(id_identidad=identidad.id)
    )
    servicio = VerificacionService(db_session)
    sesion = servicio.iniciar_sesion(credencial.codigo, None)
    sesion.rostro_coincide = True
    db_session.commit()
    return servicio, sesion


def test_desafio_se_emite_al_azar_y_admite_una_sola_repeticion(db_session, tmp_path, monkeypatch):
    servicio, sesion = _crear_sesion_con_rostro_aprobado(db_session, tmp_path, monkeypatch)
    monkeypatch.setattr(verificacion_service_module.secrets, "choice", lambda opciones: opciones[0])

    inicial = servicio.emitir_desafio_prueba_vida(sesion.id)
    repetido = servicio.emitir_desafio_prueba_vida(sesion.id)

    assert inicial.id == repetido.id
    assert repetido.accion != "PARPADEO"
    assert repetido.reintentos == 1
    with pytest.raises(DesafioPruebaVidaAgotadoError):
        servicio.emitir_desafio_prueba_vida(sesion.id)

    eventos = AuditoriaService(db_session).listar_eventos(sesion.id)
    assert {evento.tipo_evento for evento in eventos} >= {
        "DESAFIO_PRUEBA_DE_VIDA_EMITIDO",
        "DESAFIO_PRUEBA_DE_VIDA_REEMPLAZADO",
    }


def test_desafio_vencido_rechaza_y_deja_evidencia(db_session, tmp_path, monkeypatch):
    servicio, sesion = _crear_sesion_con_rostro_aprobado(db_session, tmp_path, monkeypatch)
    desafio = servicio.emitir_desafio_prueba_vida(sesion.id)
    desafio.fecha_vencimiento = verificacion_service_module._now() - verificacion_service_module.timedelta(seconds=1)
    db_session.commit()
    monkeypatch.setattr(servicio.liveness, "validar_accion", lambda *_: pytest.fail("No debe evaluar"))

    resultado = servicio.registrar_prueba_vida(sesion.id, b"captura-sintetica")

    assert (resultado.estado, resultado.resultado) == (EstadoSesion.COMPLETADA, R.PRUEBA_DE_VIDA_FALLIDA)
    assert desafio.estado == "VENCIDO"
    assert "PRUEBA_DE_VIDA_VENCIDA" in [
        evento.tipo_evento for evento in AuditoriaService(db_session).listar_eventos(sesion.id)
    ]


@pytest.mark.parametrize("medio", ["fotografia_impresa", "fotografia_en_pantalla"])
def test_ataque_estatico_controlado_es_rechazado(db_session, tmp_path, monkeypatch, medio):
    servicio, sesion = _crear_sesion_con_rostro_aprobado(db_session, tmp_path, monkeypatch)
    servicio.emitir_desafio_prueba_vida(sesion.id)
    monkeypatch.setattr(
        servicio.liveness,
        "validar_accion",
        lambda *_: (False, {"metrica": "simulada", "motivo": "ACCION_NO_DETECTADA", "experimental": True, "medio_controlado": medio}),
    )

    resultado = servicio.registrar_prueba_vida(sesion.id, b"captura-estatica")

    assert resultado.resultado == R.PRUEBA_DE_VIDA_FALLIDA
    evento = AuditoriaService(db_session).listar_eventos(sesion.id)[-2]
    assert medio in evento.detalle


def _imagen_sintetica() -> bytes:
    imagen = np.zeros((160, 160, 3), dtype=np.uint8)
    _ok, codificada = cv2.imencode(".png", imagen)
    return codificada.tobytes()


def test_liveness_rechaza_multiples_rostros(monkeypatch):
    class _Landmarker:
        def detect(self, _imagen):
            return SimpleNamespace(face_landmarks=[[], []])

    monkeypatch.setattr(liveness_service_module, "_obtener_landmarker", lambda: _Landmarker())
    with pytest.raises(RostroMultipleDetectadoError):
        LivenessService()._landmarks(_imagen_sintetica())


def test_fotografia_estatica_sin_giro_no_supera_desafio_de_giro(monkeypatch):
    puntos = [SimpleNamespace(x=0.0, y=0.0) for _ in range(500)]
    puntos[1] = SimpleNamespace(x=0.5, y=0.5)
    puntos[234] = SimpleNamespace(x=0.0, y=0.5)
    puntos[454] = SimpleNamespace(x=1.0, y=0.5)
    monkeypatch.setattr(LivenessService, "_landmarks", lambda *_: puntos)

    superado, detalle = LivenessService().validar_accion(AccionPruebaVida.GIRO_IZQUIERDA, b"estatica")

    assert superado is False
    assert detalle["motivo"] == "ACCION_NO_DETECTADA"


def test_api_emite_desafio_y_rechaza_captura_estatica(db_session, tmp_path, monkeypatch):
    servicio, sesion = _crear_sesion_con_rostro_aprobado(db_session, tmp_path, monkeypatch)
    # La ruta inicia su propia sesión; la sembrada verifica que la identidad y
    # credencial reales pueden recorrer el mismo contrato HTTP.
    credencial = db_session.get(Credencial, sesion.id_credencial)
    AuthService(db_session).create_user(
        "Operador liveness", "liveness@example.test", "clave", RolUsuario.OPERADOR
    )
    monkeypatch.setattr(BiometriaService, "comparar_rostro", lambda *_: (True, 0.99))
    monkeypatch.setattr(LivenessService, "validar_accion", lambda *_: (False, {"motivo": "ACCION_NO_DETECTADA"}))
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            login = client.post("/auth/login", json={"correo": "liveness@example.test", "password": "clave"})
            headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
            inicio = client.post("/verificaciones", json={"codigo_credencial": credencial.codigo}, headers=headers)
            id_sesion = inicio.json()["id"]
            rostro = client.post(
                f"/verificaciones/{id_sesion}/rostro",
                files={"imagen": ("rostro.jpg", b"captura", "image/jpeg")},
                headers=headers,
            )
            assert rostro.status_code == 200
            desafio = client.post(f"/verificaciones/{id_sesion}/prueba-vida/desafio", headers=headers)
            assert desafio.status_code == 200
            assert desafio.json()["accion"] in {"PARPADEO", "GIRO_IZQUIERDA", "GIRO_DERECHA"}
            vida = client.post(
                f"/verificaciones/{id_sesion}/prueba-vida",
                files={"imagen": ("vida.jpg", b"captura-estatica", "image/jpeg")},
                headers=headers,
            )
            assert (vida.status_code, vida.json()["resultado"]) == (200, R.PRUEBA_DE_VIDA_FALLIDA)
    finally:
        app.dependency_overrides.clear()
