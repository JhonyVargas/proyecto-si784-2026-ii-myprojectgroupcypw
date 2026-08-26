"""Bitácora de auditoría con encadenamiento criptográfico (RF-11, RF-12, RN-07).

Cada evento se enlaza con el anterior mediante SHA-256: el hash de un evento
incluye el hash del evento previo. Alterar cualquier campo de un evento ya
registrado rompe la cadena a partir de ese punto, lo que ``verificar_cadena``
puede detectar.
"""

from __future__ import annotations

import hashlib
import json

from sqlalchemy.orm import Session

from app.models import schemas
from app.models.db_models import EventoAuditoria, _now

GENESIS_HASH = "0" * 64


class AuditoriaService:
    def __init__(self, db: Session):
        self.db = db

    def _ultimo_evento(self) -> EventoAuditoria | None:
        return (
            self.db.query(EventoAuditoria)
            .order_by(EventoAuditoria.secuencia.desc())
            .first()
        )

    @staticmethod
    def _calcular_hash(
        id_sesion: str | None,
        tipo_evento: str,
        detalle: str,
        timestamp_iso: str,
        hash_anterior: str,
    ) -> str:
        payload = "|".join([str(id_sesion), tipo_evento, detalle, timestamp_iso, hash_anterior])
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def registrar_evento(
        self, id_sesion: str | None, tipo_evento: str, detalle: dict
    ) -> EventoAuditoria:
        anterior = self._ultimo_evento()
        hash_anterior = anterior.hash_evento_actual if anterior else GENESIS_HASH
        secuencia = (anterior.secuencia + 1) if anterior else 1

        timestamp = _now()
        timestamp_iso = timestamp.isoformat()
        detalle_json = json.dumps(detalle, sort_keys=True, ensure_ascii=False, default=str)

        hash_actual = self._calcular_hash(
            id_sesion, tipo_evento, detalle_json, timestamp_iso, hash_anterior
        )

        evento = EventoAuditoria(
            id_sesion=id_sesion,
            tipo_evento=tipo_evento,
            detalle=detalle_json,
            hash_evento_anterior=hash_anterior,
            hash_evento_actual=hash_actual,
            timestamp=timestamp,
            timestamp_iso=timestamp_iso,
            secuencia=secuencia,
        )
        self.db.add(evento)
        self.db.commit()
        self.db.refresh(evento)
        return evento

    def listar_eventos(self, id_sesion: str | None = None) -> list[EventoAuditoria]:
        query = self.db.query(EventoAuditoria).order_by(EventoAuditoria.secuencia.asc())
        if id_sesion:
            query = query.filter(EventoAuditoria.id_sesion == id_sesion)
        return query.all()

    def verificar_cadena(self) -> schemas.VerificacionCadenaRespuesta:
        eventos = self.listar_eventos()
        hash_esperado = GENESIS_HASH
        for evento in eventos:
            if evento.hash_evento_anterior != hash_esperado:
                return schemas.VerificacionCadenaRespuesta(
                    valida=False,
                    total_eventos=len(eventos),
                    primer_evento_alterado=evento.id,
                )
            hash_recalculado = self._calcular_hash(
                evento.id_sesion,
                evento.tipo_evento,
                evento.detalle,
                evento.timestamp_iso,
                evento.hash_evento_anterior,
            )
            if hash_recalculado != evento.hash_evento_actual:
                return schemas.VerificacionCadenaRespuesta(
                    valida=False,
                    total_eventos=len(eventos),
                    primer_evento_alterado=evento.id,
                )
            hash_esperado = evento.hash_evento_actual
        return schemas.VerificacionCadenaRespuesta(valida=True, total_eventos=len(eventos))
