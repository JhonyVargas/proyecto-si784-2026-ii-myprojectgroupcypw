"""Simulador de Identidad (RF-01, RF-02, RN-02, RN-03).

Representa, exclusivamente con fines académicos, una fuente institucional
externa de información de identidad. Nunca debe contener datos reales de
clientes de una notaría (RN-02): toda identidad registrada es ficticia.
"""

from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from app.core.database import DATA_DIR
from app.models import schemas
from app.models.db_models import IdentidadSimulada
from app.models.enums import EstadoIdentidad
from app.services.consentimiento_service import ConsentimientoService
from app.services.errors import ConsentimientoRequeridoError, IdentidadNoEncontradaError

REFERENCIAS_DIR = DATA_DIR / "referencias_faciales"
REFERENCIAS_DIR.mkdir(parents=True, exist_ok=True)


class IdentidadService:
    def __init__(self, db: Session):
        self.db = db
        self.consentimientos = ConsentimientoService(db)

    def registrar(
        self, datos: schemas.IdentidadCrear, imagen_referencia: bytes
    ) -> IdentidadSimulada:
        if not datos.confirmo_dato_ficticio:
            raise ValueError(
                "NotaryVerify solo admite identidades ficticias (RN-02): confirme "
                "explícitamente que los datos no corresponden a una persona real."
            )
        if not self.consentimientos.existe_consentimiento_valido(datos.id_participante):
            raise ConsentimientoRequeridoError(
                f"El participante '{datos.id_participante}' no cuenta con un "
                "consentimiento biométrico vigente (RN-03). Regístrelo antes de "
                "enrolar su rostro."
            )

        identidad = IdentidadSimulada(
            nombre_ficticio=datos.nombre_ficticio,
            documento_ficticio=datos.documento_ficticio,
            id_participante=datos.id_participante,
            referencia_facial_path="",
            estado=EstadoIdentidad.ACTIVA,
        )
        self.db.add(identidad)
        self.db.flush()

        ruta_imagen = REFERENCIAS_DIR / f"{identidad.id}.jpg"
        ruta_imagen.write_bytes(imagen_referencia)
        identidad.referencia_facial_path = str(ruta_imagen)

        self.db.commit()
        self.db.refresh(identidad)
        return identidad

    def consultar(self, id_identidad: str) -> IdentidadSimulada:
        identidad = self.db.get(IdentidadSimulada, id_identidad)
        if identidad is None:
            raise IdentidadNoEncontradaError(f"No existe la identidad '{id_identidad}'.")
        return identidad

    def bloquear(self, id_identidad: str) -> IdentidadSimulada:
        identidad = self.consultar(id_identidad)
        identidad.estado = EstadoIdentidad.BLOQUEADA
        self.db.commit()
        self.db.refresh(identidad)
        return identidad

    def referencia_facial_bytes(self, id_identidad: str) -> bytes:
        identidad = self.consultar(id_identidad)
        return Path(identidad.referencia_facial_path).read_bytes()
