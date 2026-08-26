"""Servicio de consentimiento biométrico (RF-19, RN-03)."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import schemas
from app.models.db_models import ConsentimientoBiometrico


class ConsentimientoService:
    def __init__(self, db: Session):
        self.db = db

    def otorgar(self, datos: schemas.ConsentimientoCrear) -> ConsentimientoBiometrico:
        consentimiento = ConsentimientoBiometrico(
            id_participante=datos.id_participante,
            alcance=datos.alcance,
        )
        self.db.add(consentimiento)
        self.db.commit()
        self.db.refresh(consentimiento)
        return consentimiento

    def existe_consentimiento_valido(self, id_participante: str) -> bool:
        consentimiento = (
            self.db.query(ConsentimientoBiometrico)
            .filter(
                ConsentimientoBiometrico.id_participante == id_participante,
                ConsentimientoBiometrico.revocado.is_(False),
            )
            .first()
        )
        return consentimiento is not None

    def revocar(self, id_participante: str) -> None:
        self.db.query(ConsentimientoBiometrico).filter(
            ConsentimientoBiometrico.id_participante == id_participante
        ).update({"revocado": True})
        self.db.commit()
