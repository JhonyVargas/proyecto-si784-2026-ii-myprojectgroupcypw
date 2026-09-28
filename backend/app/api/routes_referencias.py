"""Flujo de solicitud y decisión de referencias biométricas ficticias."""

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.api.auth import CurrentUser, require_roles
from app.core.database import get_db
from app.models import schemas
from app.models.db_models import Usuario
from app.models.enums import RolUsuario
from app.services.identidad_service import IdentidadService

router = APIRouter(prefix="/identidades", tags=["Cambios de referencia biométrica"])


@router.post("/{id_identidad}/referencia/solicitudes", response_model=schemas.SolicitudCambioReferenciaRespuesta, status_code=201)
def solicitar_cambio(
    id_identidad: str,
    motivo: str = Form(...),
    imagen_referencia: UploadFile = File(...),
    usuario: Usuario = Depends(require_roles(RolUsuario.OPERADOR, RolUsuario.ADMINISTRADOR)),
    db: Session = Depends(get_db),
):
    return IdentidadService(db).solicitar_cambio_referencia(id_identidad, usuario.id, motivo, imagen_referencia.file.read())


@router.get("/referencia/solicitudes", response_model=list[schemas.SolicitudCambioReferenciaRespuesta])
def listar_solicitudes(usuario: Usuario = Depends(require_roles(RolUsuario.ADMINISTRADOR)), db: Session = Depends(get_db)):
    return IdentidadService(db).listar_solicitudes_cambio_referencia()


@router.post("/referencia/solicitudes/{id_solicitud}/decision", response_model=schemas.SolicitudCambioReferenciaRespuesta)
def decidir_solicitud(
    id_solicitud: str, decision: schemas.DecisionCambioReferencia,
    usuario: Usuario = Depends(require_roles(RolUsuario.ADMINISTRADOR)), db: Session = Depends(get_db),
):
    return IdentidadService(db).decidir_cambio_referencia(id_solicitud, usuario.id, decision.aprobar, decision.motivo_decision)
