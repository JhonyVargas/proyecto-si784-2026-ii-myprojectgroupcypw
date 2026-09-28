"""Autenticación local para el entorno académico de NotaryVerify.

No proporciona cuentas institucionales ni recuperación de contraseña. Los
tokens opacos se devuelven una única vez y solo su hash se guarda en SQLite.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.db_models import SesionUsuario, Usuario, _now
from app.models.enums import RolUsuario

SESSION_DURATION = timedelta(hours=8)
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


class AuthenticationError(Exception):
    """Error intencionalmente inespecífico para no filtrar credenciales."""


def hash_password(password: str) -> str:
    """Genera una derivación scrypt con sal aleatoria para una contraseña."""
    salt = secrets.token_bytes(16)
    derived = hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P
    )
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${salt.hex()}${derived.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Verifica una derivación scrypt sin exponer diferencias temporales útiles."""
    try:
        algorithm, n, r, p, salt_hex, expected_hex = stored.split("$")
        if algorithm != "scrypt":
            return False
        derived = hashlib.scrypt(
            password.encode("utf-8"),
            salt=bytes.fromhex(salt_hex),
            n=int(n),
            r=int(r),
            p=int(p),
        )
        return hmac.compare_digest(derived.hex(), expected_hex)
    except (TypeError, ValueError):
        return False


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, nombre: str, correo: str, password: str, rol: str) -> Usuario:
        if rol not in (RolUsuario.OPERADOR, RolUsuario.ADMINISTRADOR):
            raise ValueError("Rol local no admitido.")
        if not password:
            raise ValueError("La contraseña no puede estar vacía.")
        existing = self.db.query(Usuario).filter(Usuario.correo == correo).first()
        if existing is not None:
            raise ValueError("Ya existe un usuario con ese correo.")
        usuario = Usuario(nombre=nombre, correo=correo, rol=rol, password_hash=hash_password(password))
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def login(self, correo: str, password: str) -> tuple[str, SesionUsuario, Usuario]:
        usuario = self.db.query(Usuario).filter(Usuario.correo == correo).first()
        if usuario is None or not verify_password(password, usuario.password_hash):
            raise AuthenticationError()
        token = secrets.token_urlsafe(32)
        session = SesionUsuario(
            id_usuario=usuario.id,
            token_hash=hashlib.sha256(token.encode("utf-8")).hexdigest(),
            fecha_expiracion=_now() + SESSION_DURATION,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return token, session, usuario

    def current_user(self, token: str) -> Usuario:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        session = self.db.query(SesionUsuario).filter(SesionUsuario.token_hash == token_hash).first()
        if session is None or session.fecha_revocacion is not None or session.fecha_expiracion <= _now():
            raise AuthenticationError()
        usuario = self.db.get(Usuario, session.id_usuario)
        if usuario is None:
            raise AuthenticationError()
        return usuario

    def logout(self, token: str) -> None:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        session = self.db.query(SesionUsuario).filter(SesionUsuario.token_hash == token_hash).first()
        if session is None or session.fecha_revocacion is not None or session.fecha_expiracion <= _now():
            raise AuthenticationError()
        session.fecha_revocacion = _now()
        self.db.commit()


def bootstrap_from_environment(db: Session) -> None:
    """Crea usuarios *solo* cuando todas las variables de cada cuenta existen."""
    for prefix, role, name in (
        ("NOTARYVERIFY_BOOTSTRAP_OPERATOR", RolUsuario.OPERADOR, "Operador de desarrollo"),
        ("NOTARYVERIFY_BOOTSTRAP_ADMIN", RolUsuario.ADMINISTRADOR, "Administrador de desarrollo"),
    ):
        correo = os.getenv(f"{prefix}_EMAIL")
        password = os.getenv(f"{prefix}_PASSWORD")
        configured = [value for value in (correo, password) if value]
        if configured and len(configured) != 2:
            raise RuntimeError(f"Configure tanto {prefix}_EMAIL como {prefix}_PASSWORD, o ninguna.")
        if not configured:
            continue
        if db.query(Usuario).filter(Usuario.correo == correo).first() is None:
            AuthService(db).create_user(name, correo, password, role)
