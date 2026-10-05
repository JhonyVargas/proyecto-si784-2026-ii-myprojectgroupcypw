"""Motor de reglas de seguridad multicapa (RF-07/RF-08, RN-01).

Ningún factor evaluado de forma aislada es suficiente para aprobar una
identidad: se exige una credencial registrada y no revocada, coincidencia
facial y una prueba de vida superada. Los resultados posibles replican
exactamente el catálogo definido en el FD01/FD02 del proyecto.
"""

from __future__ import annotations

import json

from sqlalchemy.orm import Session

from app.models.db_models import ConfiguracionReglas, DecisionReglas, SesionVerificacion, _now
from app.models.enums import ResultadoVerificacion as R

CATALOGO = ("CREDENCIAL", "ROSTRO", "PRUEBA_VIDA")
PRIORIDADES_BASE = list(CATALOGO)


class ReglasService:
    def __init__(self, db: Session | None = None):
        self.db = db

    @staticmethod
    def validar_prioridades(prioridades: list[str]) -> list[str]:
        if sorted(prioridades) != sorted(CATALOGO) or len(prioridades) != len(CATALOGO):
            raise ValueError("Las prioridades deben contener exactamente CREDENCIAL, ROSTRO y PRUEBA_VIDA.")
        return prioridades

    def activa(self) -> ConfiguracionReglas | None:
        return None if self.db is None else self.db.query(ConfiguracionReglas).order_by(ConfiguracionReglas.version.desc()).first()

    def crear_configuracion(self, prioridades: list[str], id_actor: str) -> ConfiguracionReglas:
        if self.db is None:
            raise RuntimeError("La configuración requiere persistencia.")
        prioridades = self.validar_prioridades(prioridades)
        ultima = self.activa()
        configuracion = ConfiguracionReglas(version=(ultima.version + 1) if ultima else 1, prioridades=json.dumps(prioridades), creada_por=id_actor)
        self.db.add(configuracion)
        self.db.commit()
        self.db.refresh(configuracion)
        return configuracion

    def prioridades_aplicables(self) -> tuple[list[str], ConfiguracionReglas | None]:
        configuracion = self.activa()
        return (json.loads(configuracion.prioridades) if configuracion else PRIORIDADES_BASE, configuracion)

    def evaluar(
        self,
        credencial_registrada: bool,
        credencial_revocada: bool,
        rostro_coincide: bool | None,
        prueba_vida_superada: bool | None,
    ) -> str:
        prioridades, _ = self.prioridades_aplicables()
        fallos = {
            "CREDENCIAL": R.CREDENCIAL_NO_REGISTRADA if not credencial_registrada else (R.CREDENCIAL_REVOCADA if credencial_revocada else None),
            "ROSTRO": R.ROSTRO_NO_COINCIDENTE if rostro_coincide is False else None,
            "PRUEBA_VIDA": R.PRUEBA_DE_VIDA_FALLIDA if prueba_vida_superada is False else None,
        }
        for factor in prioridades:
            if fallos[factor]:
                return fallos[factor]
        return R.IDENTIDAD_VERIFICADA if rostro_coincide is True and prueba_vida_superada is True else R.REQUIERE_REVISION

    def registrar_decision(self, sesion: SesionVerificacion, resultado: str) -> None:
        if self.db is None or self.db.query(DecisionReglas).filter_by(id_sesion=sesion.id).first():
            return
        prioridades, configuracion = self.prioridades_aplicables()
        if configuracion is None:
            configuracion = self.crear_configuracion(PRIORIDADES_BASE, sesion.id_responsable or "SISTEMA")
            prioridades = PRIORIDADES_BASE
        self.db.add(DecisionReglas(id_sesion=sesion.id, id_configuracion=configuracion.id, configuracion_aplicada=json.dumps({"version": configuracion.version, "prioridades": prioridades}), resultado=resultado, fecha_decision=_now()))
        self.db.commit()
