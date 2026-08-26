"""Motor de reglas de seguridad multicapa (RF-07/RF-08, RN-01).

Ningún factor evaluado de forma aislada es suficiente para aprobar una
identidad: se exige una credencial registrada y no revocada, coincidencia
facial y una prueba de vida superada. Los resultados posibles replican
exactamente el catálogo definido en el FD01/FD02 del proyecto.
"""

from __future__ import annotations

from typing import Optional

from app.models.enums import ResultadoVerificacion as R


class ReglasService:
    def evaluar(
        self,
        credencial_registrada: bool,
        credencial_revocada: bool,
        rostro_coincide: Optional[bool],
        prueba_vida_superada: Optional[bool],
    ) -> str:
        if not credencial_registrada:
            return R.CREDENCIAL_NO_REGISTRADA
        if credencial_revocada:
            return R.CREDENCIAL_REVOCADA
        if rostro_coincide is False:
            return R.ROSTRO_NO_COINCIDENTE
        if prueba_vida_superada is False:
            return R.PRUEBA_DE_VIDA_FALLIDA
        if rostro_coincide is True and prueba_vida_superada is True:
            return R.IDENTIDAD_VERIFICADA
        return R.REQUIERE_REVISION
