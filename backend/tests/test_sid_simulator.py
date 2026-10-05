import pytest

from app.models.db_models import SesionVerificacion
from app.models.enums import ResultadoVerificacion as R
from app.services.auditoria_service import AuditoriaService
from app.services.errors import TramiteNoHabilitadoError
from app.services.sid_sunarp_service import SidSunarpSimuladoService


@pytest.mark.parametrize("escenario,estado", [
    ("DISPONIBLE", "ENVIADO"), ("RECHAZADO", "RECHAZADO"),
    ("SERVICIO_NO_DISPONIBLE", "ERROR_SERVICIO"), ("TIEMPO_AGOTADO", "TIEMPO_AGOTADO"),
    ("RESPUESTA_INVALIDA", "RESPUESTA_INVALIDA"), ("ERROR_INTERNO", "ERROR_INTERNO"),
])
def test_escenarios_sid_son_deterministas_y_auditados(db_session, escenario, estado):
    sesion = SesionVerificacion(resultado=R.IDENTIDAD_VERIFICADA)
    db_session.add(sesion); db_session.commit()
    tramite = SidSunarpSimuladoService(db_session).enviar_tramite(sesion.id, escenario)
    assert tramite.estado == estado
    assert "TRAMITE_SIMULADO_EVALUADO" in [e.tipo_evento for e in AuditoriaService(db_session).listar_eventos(sesion.id)]


def test_sesion_no_aprobada_no_invoca_simulador(db_session):
    sesion = SesionVerificacion(resultado=R.PRUEBA_DE_VIDA_FALLIDA)
    db_session.add(sesion); db_session.commit()
    with pytest.raises(TramiteNoHabilitadoError):
        SidSunarpSimuladoService(db_session).enviar_tramite(sesion.id)
    assert not AuditoriaService(db_session).listar_eventos(sesion.id)
