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
from app.models.db_models import EventoAuditoria, SesionVerificacion, _now
from app.services.errors import SesionNoEncontradaError

GENESIS_HASH = "0" * 64

# Catálogo de evidencia pública de operaciones críticas.  Los detalles crudos
# se conservan únicamente para el cálculo de la cadena y no se devuelven por
# este contrato; en particular, no se expone el código de credencial ni datos
# biométricos de los eventos históricos.
_PAYLOAD_PUBLICO = {
    "SESION_INICIADA": (),
    "ROSTRO_EVALUADO": ("coincide",),
    "DESAFIO_PRUEBA_DE_VIDA_EMITIDO": ("reintentos", "experimental"),
    "DESAFIO_PRUEBA_DE_VIDA_REEMPLAZADO": ("reintentos", "experimental"),
    "PRUEBA_DE_VIDA_EVALUADA": ("superado", "experimental"),
    "PRUEBA_DE_VIDA_VENCIDA": ("motivo", "experimental"),
    "SESION_FINALIZADA": ("resultado",),
    "SESION_EXPIRADA": ("origen",),
    "EVIDENCIA_TRAMITE_ASOCIADA": ("id_documento", "id_tramite", "resultado_sesion"),
    "TRAMITE_SIMULADO_EVALUADO": ("id_documento", "id_tramite", "escenario", "estado", "respuesta_minima"),
}


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

    @staticmethod
    def _resumen_evento(evento: EventoAuditoria) -> schemas.EventoReconstruidoRespuesta:
        """Normaliza detalle histórico a un contrato mínimo de auditoría."""
        try:
            detalle = json.loads(evento.detalle)
        except json.JSONDecodeError:
            detalle = {}
        campos = _PAYLOAD_PUBLICO.get(evento.tipo_evento, ())
        payload = {campo: detalle.get(campo) for campo in campos if campo in detalle}
        id_entidad = str(
            detalle.get("id_tramite") or detalle.get("id_documento") or evento.id_sesion or "SISTEMA"
        )
        entidad = (
            "TRAMITE_SIMULADO" if "id_tramite" in detalle
            else "DOCUMENTO" if "id_documento" in detalle
            else "SESION_VERIFICACION" if evento.id_sesion
            else "SISTEMA"
        )
        actor = str(
            detalle.get("actor")
            or detalle.get("id_administrador")
            or detalle.get("id_decisor")
            or "SISTEMA"
        )
        return schemas.EventoReconstruidoRespuesta(
            tipo_evento=evento.tipo_evento,
            actor=actor,
            entidad=entidad,
            id_entidad=id_entidad,
            payload_minimo=payload,
            timestamp=evento.timestamp,
            secuencia=evento.secuencia,
        )

    def reconstruir_sesion(self, id_sesion: str) -> schemas.ReconstruccionSesionRespuesta:
        if self.db.get(SesionVerificacion, id_sesion) is None:
            raise SesionNoEncontradaError(f"No existe la sesión '{id_sesion}'.")
        eventos = self.listar_eventos(id_sesion)
        return schemas.ReconstruccionSesionRespuesta(
            id_sesion=id_sesion,
            eventos=[self._resumen_evento(evento) for evento in eventos],
        )

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
