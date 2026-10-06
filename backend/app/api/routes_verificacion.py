"""Endpoints del flujo de verificación multicapa (CU-03, RF-05 a RF-08)."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.seguridad import leer_imagen
from app.api.auth import CurrentUser, require_roles
from app.models.db_models import Usuario
from app.models.enums import RolUsuario
from app.models import schemas
from app.services.verificacion_service import VerificacionService

router = APIRouter(prefix="/verificaciones", tags=["Verificación multicapa"])


@router.post("", response_model=schemas.SesionRespuesta, status_code=201)
def iniciar_verificacion(
    datos: schemas.SesionIniciar,
    usuario: Usuario = Depends(require_roles(RolUsuario.OPERADOR, RolUsuario.ADMINISTRADOR)),
    db: Session = Depends(get_db),
):
    # El responsable procede exclusivamente de la sesión autenticada.
    return VerificacionService(db).iniciar_sesion(datos.codigo_credencial, usuario.id)


@router.get("", response_model=list[schemas.SesionHistorialRespuesta])
def listar_verificaciones(
    resultado: str | None = None,
    fecha_desde: datetime | None = Query(default=None),
    fecha_hasta: datetime | None = Query(default=None),
    id_identidad: str | None = None,
    usuario: Usuario = Depends(require_roles(RolUsuario.ADMINISTRADOR)),
    db: Session = Depends(get_db),
):
    """Historial filtrable para Administrador, sin exponer muestras biométricas."""
    return VerificacionService(db).listar_sesiones(resultado, fecha_desde, fecha_hasta, id_identidad)


@router.get("/alertas", response_model=list[schemas.AlertaIntentosRespuesta])
def listar_alertas(
    usuario: Usuario = Depends(require_roles(RolUsuario.ADMINISTRADOR)),
    db: Session = Depends(get_db),
):
    return VerificacionService(db).listar_alertas()


@router.post("/alertas/{id_alerta}/reactivar", response_model=schemas.AlertaIntentosRespuesta)
def reactivar_alerta(
    id_alerta: str,
    usuario: Usuario = Depends(require_roles(RolUsuario.ADMINISTRADOR)),
    db: Session = Depends(get_db),
):
    return VerificacionService(db).resolver_alerta(id_alerta, usuario.id)


@router.post("/{id_sesion}/rostro", response_model=schemas.SesionRespuesta)
def capturar_rostro(
    id_sesion: str, imagen: UploadFile = File(...),
    usuario: Usuario = Depends(require_roles(RolUsuario.OPERADOR, RolUsuario.ADMINISTRADOR)),
    db: Session = Depends(get_db)
):
    return VerificacionService(db).registrar_captura_facial(id_sesion, leer_imagen(imagen))


@router.post("/{id_sesion}/prueba-vida/desafio", response_model=schemas.DesafioPruebaVidaRespuesta)
def emitir_desafio_prueba_vida(
    id_sesion: str,
    usuario: Usuario = Depends(require_roles(RolUsuario.OPERADOR, RolUsuario.ADMINISTRADOR)),
    db: Session = Depends(get_db),
):
    """Genera el desafío aleatorio, temporal y experimental de la sesión."""
    return VerificacionService(db).emitir_desafio_prueba_vida(id_sesion)


@router.post("/{id_sesion}/prueba-vida", response_model=schemas.SesionRespuesta)
def ejecutar_prueba_vida(
    id_sesion: str,
    imagen: UploadFile = File(...),
    usuario: Usuario = Depends(require_roles(RolUsuario.OPERADOR, RolUsuario.ADMINISTRADOR)),
    db: Session = Depends(get_db),
):
    return VerificacionService(db).registrar_prueba_vida(id_sesion, leer_imagen(imagen))
