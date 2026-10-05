import json

import pytest
from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.models.db_models import DecisionReglas, SesionVerificacion
from app.models.enums import RolUsuario, ResultadoVerificacion as R
from app.services.auth_service import AuthService
from app.services.reglas_service import ReglasService


def test_configuracion_invalida_no_se_persiste(db_session):
    with pytest.raises(ValueError):
        ReglasService(db_session).crear_configuracion(["CREDENCIAL", "ROSTRO"], "actor")
    assert ReglasService(db_session).activa() is None


def test_prioridad_versionada_se_aplica_y_se_persiste_en_decision(db_session):
    reglas = ReglasService(db_session)
    configuracion = reglas.crear_configuracion(["PRUEBA_VIDA", "ROSTRO", "CREDENCIAL"], None)
    sesion = SesionVerificacion()
    db_session.add(sesion)
    db_session.commit()
    resultado = reglas.evaluar(True, False, False, False)
    reglas.registrar_decision(sesion, resultado)
    decision = db_session.query(DecisionReglas).filter_by(id_sesion=sesion.id).one()
    assert resultado == R.PRUEBA_DE_VIDA_FALLIDA
    assert decision.id_configuracion == configuracion.id
    assert json.loads(decision.configuracion_aplicada)["version"] == configuracion.version


def test_administrador_y_auditor_pueden_versionar_configuracion(db_session):
    administrador = AuthService(db_session).create_user("Admin", "rules-admin@example.test", "clave", RolUsuario.ADMINISTRADOR)
    auditor = AuthService(db_session).create_user("Auditor", "rules-auditor@example.test", "clave", RolUsuario.AUDITOR)
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as client:
            for usuario in (administrador, auditor):
                token, _, _ = AuthService(db_session).login(usuario.correo, "clave")
                respuesta = client.post("/reglas/configuracion", json={"prioridades": ["ROSTRO", "CREDENCIAL", "PRUEBA_VIDA"]}, headers={"Authorization": f"Bearer {token}"})
                assert respuesta.status_code == 201
            operador = AuthService(db_session).create_user("Operador", "rules-operator@example.test", "clave", RolUsuario.OPERADOR)
            token, _, _ = AuthService(db_session).login(operador.correo, "clave")
            assert client.post("/reglas/configuracion", json={"prioridades": ["ROSTRO", "CREDENCIAL", "PRUEBA_VIDA"]}, headers={"Authorization": f"Bearer {token}"}).status_code == 403
    finally:
        app.dependency_overrides.clear()
