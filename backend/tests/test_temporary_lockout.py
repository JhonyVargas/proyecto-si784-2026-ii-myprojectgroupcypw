from datetime import timedelta

import pytest

from app.models.db_models import AlertaIntentosFallidos, SesionVerificacion, _now
from app.models.enums import EstadoSesion, ResultadoVerificacion as R
from app.services.errors import IdentidadTemporalmenteBloqueadaError
from app.services.verificacion_service import VerificacionService


def test_three_consecutive_failures_create_traceable_temporary_lock(db_session):
    identity_id = "identity-for-lock"
    for _ in range(3):
        db_session.add(SesionVerificacion(id_identidad=identity_id, estado=EstadoSesion.COMPLETADA, resultado=R.ROSTRO_NO_COINCIDENTE, fecha_fin=_now()))
    db_session.commit()
    service = VerificacionService(db_session)
    service._evaluar_intentos_fallidos(identity_id)

    alert = db_session.query(AlertaIntentosFallidos).one()
    assert alert.intentos_consecutivos == 3
    assert alert.fecha_resolucion is None
    with pytest.raises(IdentidadTemporalmenteBloqueadaError):
        service._comprobar_bloqueo_temporal(identity_id)

    alert.bloqueada_hasta = _now() - timedelta(seconds=1)
    db_session.commit()
    service._comprobar_bloqueo_temporal(identity_id)
    assert alert.fecha_resolucion is not None
