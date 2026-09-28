"""Dependencias de autenticación para las rutas de NotaryVerify."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.db_models import Usuario
from app.services.auth_service import AuthService, AuthenticationError

bearer_scheme = HTTPBearer(auto_error=False)


def authentication_required() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"code": "AUTHENTICATION_REQUIRED", "message": "Autenticación requerida."},
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Session = Depends(get_db),
) -> Usuario:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise authentication_required()
    try:
        return AuthService(db).current_user(credentials.credentials)
    except AuthenticationError as exc:
        raise authentication_required() from exc


CurrentUser = Annotated[Usuario, Depends(get_current_user)]
