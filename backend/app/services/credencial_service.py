"""Credenciales de prueba QR/RFID (RF-03, RF-04, RN-04).

La lectura de una credencial únicamente permite recuperar el registro que
corresponde verificar; por sí sola nunca aprueba una identidad (ver
``ReglasService``).
"""

from __future__ import annotations

import io
import secrets
from typing import Protocol

import qrcode
from sqlalchemy.orm import Session

from app.models import schemas
from app.models.db_models import Credencial
from app.models.enums import EstadoCredencial, TipoCredencial
from app.services.errors import CredencialNoRegistradaError


class LectorRfid(Protocol):
    """Puerto para lectores RFID; una integración física futura lo implementará."""

    def leer(self, uid: str) -> str: ...


class AdaptadorRfidSimulado:
    """Lector determinista de UID sintéticos, sin depender de hardware físico."""

    @staticmethod
    def leer(uid: str) -> str:
        if not uid or any(character not in "0123456789ABCDEF" for character in uid):
            raise ValueError("UID RFID inválido: use hexadecimal en mayúsculas sin separadores (ejemplo: 04A1B2C3).")
        return uid


class CredencialService:
    def __init__(self, db: Session):
        self.db = db

    def emitir(self, datos: schemas.CredencialCrear) -> Credencial:
        if datos.tipo not in (TipoCredencial.QR, TipoCredencial.RFID):
            raise ValueError("Tipo de credencial no admitido: use QR o RFID.")
        if datos.tipo == TipoCredencial.RFID:
            if datos.uid_rfid is None:
                raise ValueError("Una credencial RFID simulada requiere uid_rfid.")
            codigo = AdaptadorRfidSimulado.leer(datos.uid_rfid)
        else:
            if datos.uid_rfid is not None:
                raise ValueError("uid_rfid solo se admite para credenciales RFID.")
            codigo = f"NV-{secrets.token_hex(6).upper()}"
        credencial = Credencial(
            codigo=codigo,
            tipo=datos.tipo,
            id_identidad=datos.id_identidad,
            estado=EstadoCredencial.ACTIVA,
        )
        self.db.add(credencial)
        self.db.commit()
        self.db.refresh(credencial)
        return credencial

    def listar(self) -> list[Credencial]:
        """Todas las credenciales emitidas, de la más reciente a la más antigua."""
        return (
            self.db.query(Credencial)
            .order_by(Credencial.fecha_emision.desc())
            .all()
        )

    def leer(self, codigo: str) -> Credencial:
        credencial = self.db.query(Credencial).filter(Credencial.codigo == codigo).first()
        if credencial is None:
            raise CredencialNoRegistradaError(f"La credencial '{codigo}' no está registrada.")
        return credencial

    def leer_rfid(self, uid: str, lector: LectorRfid | None = None) -> Credencial:
        """Recupera la credencial RFID por el mismo contrato que QR, sin aprobarla."""
        codigo = (lector or AdaptadorRfidSimulado()).leer(uid)
        credencial = self.leer(codigo)
        if credencial.tipo != TipoCredencial.RFID:
            raise CredencialNoRegistradaError(f"El UID RFID '{uid}' no está asociado a una credencial RFID.")
        return credencial

    def revocar(self, id_credencial: str) -> Credencial:
        credencial = self.db.get(Credencial, id_credencial)
        if credencial is None:
            raise CredencialNoRegistradaError(f"No existe la credencial '{id_credencial}'.")
        credencial.estado = EstadoCredencial.REVOCADA
        self.db.commit()
        self.db.refresh(credencial)
        return credencial

    def generar_imagen_qr(self, credencial: Credencial) -> bytes:
        imagen = qrcode.make(credencial.codigo)
        buffer = io.BytesIO()
        imagen.save(buffer, format="PNG")
        return buffer.getvalue()
