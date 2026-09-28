"""Rutas de sesión local para los roles del prototipo académico."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.api.auth import CurrentUser, authentication_required, bearer_scheme
from app.core.database import get_db
from app.models import schemas
from app.services.auth_service import AuthService, AuthenticationError

router = APIRouter(prefix="/auth", tags=["Autenticación local"])


def _usuario_respuesta(usuario) -> schemas.UsuarioAutenticadoRespuesta:
    return schemas.UsuarioAutenticadoRespuesta(
        id=usuario.id, nombre=usuario.nombre, correo=usuario.correo, rol=usuario.rol
    )


@router.post("/login", response_model=schemas.LoginRespuesta)
def login(datos: schemas.LoginSolicitud, db: Session = Depends(get_db)):
    try:
        token, session, usuario = AuthService(db).login(datos.correo, datos.password)
    except AuthenticationError as exc:
        raise authentication_required() from exc
    return schemas.LoginRespuesta(
        access_token=token, expires_at=session.fecha_expiracion, usuario=_usuario_respuesta(usuario)
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise authentication_required()
    try:
        AuthService(db).logout(credentials.credentials)
    except AuthenticationError as exc:
        raise authentication_required() from exc


@router.get("/me", response_model=schemas.UsuarioAutenticadoRespuesta)
def current_user(usuario: CurrentUser):
    return _usuario_respuesta(usuario)
