# Orden recomendado y ruta crítica

## Ruta crítica del MVP

1. [#4](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/4) autenticación.
2. [#5](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/5) autorización y [#6](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/6) contratos API.
3. [#7](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/7) sesiones; luego [#8](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/8) alertas.
4. [#9](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/9) experiencia del operador.
5. [#10](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/10) evidencia de los cuatro escenarios.

## Blockers

- #4 bloquea acceso seguro a datos y operaciones sensibles.
- #11 requiere decisión real sobre hardware RFID, pero no bloquea QR/MVP.
- #28 espera evidencia de implementación y evaluación; no debe cerrarse por planificación sola.

## Paralelizables

Mientras la ruta MVP avanza, pueden comenzar #6 (contratos), #14 (liveness), #18 (confianza facial), #21 (persistencia) y #23 (CI). Sus resultados se integran solo a través de sus dependencias documentadas.

## Regla de ejecución

Cada issue sigue: propuesta OpenSpec cuando cambie comportamiento significativo, rama focalizada, implementación, pruebas, documentación/evidencia, actualización de issue y pull request. Una prueba no ejecutada debe registrar comando, motivo y riesgo; ninguna issue se cierra por el mero hecho de estar planificada.
