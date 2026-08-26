"""Modelos ORM (SQLAlchemy) que representan los objetos del dominio descritos
en el FD03 (SRS), sección 5.3.1 - Análisis de Objetos del Dominio.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import (
    EstadoCredencial,
    EstadoIdentidad,
    EstadoSesion,
    EstadoTramite,
    RolUsuario,
    TipoCredencial,
)


def _uuid() -> str:
    return uuid.uuid4().hex


def _now() -> datetime:
    """Fecha/hora actual en UTC, sin tzinfo.

    Se guarda siempre "naive" (sin zona horaria) a propósito: SQLite no tiene
    un tipo de dato nativo para timestamps con zona horaria, por lo que
    mezclar datetimes "aware" y "naive" en el mismo proceso puede producir
    comparaciones inconsistentes tras leer un valor de vuelta desde la base
    de datos. Se asume UTC de forma consistente en todo el sistema.
    """

    return datetime.now(timezone.utc).replace(tzinfo=None)


class ConsentimientoBiometrico(Base):
    __tablename__ = "consentimientos_biometricos"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    id_participante: Mapped[str] = mapped_column(String(120), index=True)
    alcance: Mapped[str] = mapped_column(Text)
    fecha_otorgado: Mapped[datetime] = mapped_column(DateTime, default=_now)
    revocado: Mapped[bool] = mapped_column(Boolean, default=False)


class IdentidadSimulada(Base):
    __tablename__ = "identidades_simuladas"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    nombre_ficticio: Mapped[str] = mapped_column(String(150))
    documento_ficticio: Mapped[str] = mapped_column(String(30), unique=True)
    id_participante: Mapped[str] = mapped_column(String(120))
    referencia_facial_path: Mapped[str] = mapped_column(String(255), default="")
    estado: Mapped[str] = mapped_column(String(20), default=EstadoIdentidad.ACTIVA)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=_now)

    credenciales: Mapped[list["Credencial"]] = relationship(back_populates="identidad")


class Credencial(Base):
    __tablename__ = "credenciales"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tipo: Mapped[str] = mapped_column(String(10), default=TipoCredencial.QR)
    id_identidad: Mapped[str] = mapped_column(ForeignKey("identidades_simuladas.id"))
    estado: Mapped[str] = mapped_column(String(20), default=EstadoCredencial.ACTIVA)
    fecha_emision: Mapped[datetime] = mapped_column(DateTime, default=_now)

    identidad: Mapped["IdentidadSimulada"] = relationship(back_populates="credenciales")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    nombre: Mapped[str] = mapped_column(String(120))
    correo: Mapped[str] = mapped_column(String(150), unique=True)
    rol: Mapped[str] = mapped_column(String(20), default=RolUsuario.OPERADOR)
    password_hash: Mapped[str] = mapped_column(String(128))


class SesionVerificacion(Base):
    __tablename__ = "sesiones_verificacion"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    id_identidad: Mapped[str | None] = mapped_column(
        ForeignKey("identidades_simuladas.id"), nullable=True
    )
    id_credencial: Mapped[str | None] = mapped_column(
        ForeignKey("credenciales.id"), nullable=True
    )
    id_responsable: Mapped[str | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )

    rostro_coincide: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    confianza_facial: Mapped[float | None] = mapped_column(Float, nullable=True)
    prueba_vida_accion: Mapped[str | None] = mapped_column(String(20), nullable=True)
    prueba_vida_superada: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    resultado: Mapped[str | None] = mapped_column(String(40), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default=EstadoSesion.EN_CURSO)

    fecha_inicio: Mapped[datetime] = mapped_column(DateTime, default=_now)
    fecha_fin: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class EventoAuditoria(Base):
    """Evento de la bitácora de auditoría con encadenamiento criptográfico (RN-07).

    ``timestamp_iso`` guarda exactamente la cadena de texto usada para
    calcular ``hash_evento_actual``. Se persiste de forma explícita (en vez
    de recalcularla desde ``timestamp`` al leer el registro) para que la
    verificación de la cadena de hashes sea determinista, sin depender de
    cómo cada motor de base de datos serialice los valores ``datetime``.
    """

    __tablename__ = "eventos_auditoria"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    id_sesion: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    tipo_evento: Mapped[str] = mapped_column(String(60))
    detalle: Mapped[str] = mapped_column(Text)
    hash_evento_anterior: Mapped[str] = mapped_column(String(64))
    hash_evento_actual: Mapped[str] = mapped_column(String(64), unique=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=_now)
    timestamp_iso: Mapped[str] = mapped_column(String(40))
    secuencia: Mapped[int] = mapped_column(Integer, default=0)


class DocumentoVerificado(Base):
    __tablename__ = "documentos_verificados"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    id_sesion: Mapped[str] = mapped_column(String(32), index=True)
    hash_sha256: Mapped[str] = mapped_column(String(64))
    qr_verificacion: Mapped[str] = mapped_column(String(255), default="")
    contenido_path: Mapped[str] = mapped_column(String(255))
    fecha_generacion: Mapped[datetime] = mapped_column(DateTime, default=_now)


class TramiteSimulado(Base):
    __tablename__ = "tramites_simulados"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    id_sesion: Mapped[str] = mapped_column(String(32), index=True)
    estado: Mapped[str] = mapped_column(String(20), default=EstadoTramite.ENVIADO)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=_now)
