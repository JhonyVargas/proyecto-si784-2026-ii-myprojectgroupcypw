"""Configuración versionada del motor de reglas (RF-16)."""

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import require_roles
from app.core.database import get_db
from app.models import schemas
from app.models.db_models import Usuario
from app.models.enums import RolUsuario
from app.services.auditoria_service import AuditoriaService
from app.services.reglas_service import ReglasService

router = APIRouter(prefix="/reglas", tags=["Reglas configurables"])


def _respuesta(configuracion):
    return {**{"id": configuracion.id, "version": configuracion.version, "creada_por": configuracion.creada_por, "fecha_creacion": configuracion.fecha_creacion}, "prioridades": json.loads(configuracion.prioridades)}


@router.get("/configuracion", response_model=schemas.ConfiguracionReglasRespuesta)
def obtener_configuracion(usuario: Usuario = Depends(require_roles(RolUsuario.ADMINISTRADOR, RolUsuario.AUDITOR)), db: Session = Depends(get_db)):
    servicio = ReglasService(db)
    configuracion = servicio.activa()
    if configuracion is None:
        configuracion = servicio.crear_configuracion(["CREDENCIAL", "ROSTRO", "PRUEBA_VIDA"], None)
    return _respuesta(configuracion)


@router.post("/configuracion", response_model=schemas.ConfiguracionReglasRespuesta, status_code=201)
def crear_configuracion(datos: schemas.ConfiguracionReglasCrear, usuario: Usuario = Depends(require_roles(RolUsuario.ADMINISTRADOR, RolUsuario.AUDITOR)), db: Session = Depends(get_db)):
    configuracion = ReglasService(db).crear_configuracion(datos.prioridades, usuario.id)
    AuditoriaService(db).registrar_evento(None, "REGLAS_CONFIGURADAS", {"version": configuracion.version, "prioridades": datos.prioridades, "actor": usuario.id})
    return _respuesta(configuracion)
