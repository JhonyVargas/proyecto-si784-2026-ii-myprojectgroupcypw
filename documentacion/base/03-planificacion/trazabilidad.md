# Matriz de trazabilidad ejecutable

Fuente académica: `documentacion/proyecto-si784-2026-ii-myprojectgroupcypw/FD03-Informe-SRS.md`.
Los números de issue son reales y se consultan en `https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/<n>`. “Parcial” significa que hay código o pruebas iniciales, no que el requisito esté cerrado.

## Requerimientos funcionales

| Requisito | Issue(s) | Módulo / prueba o evidencia | Estado base |
| --- | --- | --- | --- |
| RF-01 identidad simulada | #4, #5, #10 | `identidad_service`, `test_credencial_flujo` | Parcial |
| RF-02 consultar identidad | #6, #10 | rutas de identidades/credenciales, API smoke | Parcial |
| RF-03 emitir credencial QR/RFID | #10, #11 | `credencial_service`, pruebas de flujo | QR parcial; RFID pendiente |
| RF-04 leer credencial | #6, #10, #11 | rutas de credenciales, reglas | Parcial |
| RF-05 capturar y comparar rostro | #18, #24, #26 | `biometria_service`, pruebas biométricas | Parcial |
| RF-06 prueba de vida | #14, #24, #27 | `liveness_service`, pruebas de liveness | Parcial |
| RF-07 motor de reglas | #10, #13 | `reglas_service`, `test_reglas_service` | Parcial/configuración pendiente |
| RF-08 sesión de verificación | #7, #8, #10, #16 | `verificacion_service`, pruebas de flujo | Parcial |
| RF-09 hash e integridad documental | #15, #16 | `documento_service`, `test_documento_integridad` | Parcial |
| RF-10 QR documental | #15 | servicio documental y consulta planificada | Parcial |
| RF-11 auditoría encadenada | #16, #17 | `auditoria_service`, hash chain | Parcial |
| RF-12 detectar alteración | #17 | `test_auditoria_hashchain` | Parcial |
| RF-13 trámite SID simulado | #16, #19, #20 | `sid_sunarp_service` | Parcial |
| RF-14 escenarios de servicio externo | #19, #20 | rutas de trámites, pruebas planificadas | Parcial |
| RF-15 autenticación | #4, #5 | modelo Usuario existente; pruebas planificadas | No iniciada |
| RF-16 configurar reglas | #13 | reglas/administración planificada | No iniciada |
| RF-17 consultar bitácora | #5, #17 | rutas de auditoría, permisos planificados | Parcial |
| RF-18 filtrar sesiones | #7 | historial y filtros planificados | No iniciada |
| RF-19 consentimiento biométrico | #5, #12, #26 | `consentimiento_service`, pruebas de flujo | Parcial |

## Requerimientos no funcionales

| Requisito | Issue(s) | Evidencia esperada | Estado base |
| --- | --- | --- | --- |
| RNF-01 cuatro pasos/usabilidad | #9, #10 | recorrido UI y tasa de éxito documentada | Parcial |
| RNF-02 comparación < 3 s | #18, #24 | 20 comparaciones medidas | Pendiente |
| RNF-03 disponibilidad 95 % | #23, #25 | healthcheck y reporte de uptime | Pendiente |
| RNF-04 flujo < 45 s | #10, #14, #24 | 20 sesiones medidas | Pendiente |
| RNF-05 FPR combinado < 5 % | #18, #26, #27 | protocolo y métricas agregadas | Pendiente |
| RNF-06 autenticación y acceso | #4, #5, #22 | pruebas 401/403 | No iniciada |
| RNF-07 HTTPS/TLS | #22 | configuración de staging y guía | Pendiente |
| RNF-08 navegadores vigentes | #9, #25 | matriz Chrome/Edge/Firefox | Pendiente |
| RNF-09 mantenibilidad | #6, #21, #23 | capas, documentación y CI | Parcial |
| RNF-10 recuperación de auditoría | #16, #17 | reconstrucción y alteración controlada | Parcial |

## Reglas de negocio

| Regla | Issue(s) | Evidencia esperada | Estado base |
| --- | --- | --- | --- |
| RN-01 ningún factor aprueba solo | #10, #13 | casos de reglas y configuración válida | Parcial |
| RN-02 identidad ficticia | #10, #22, #26 | validación y protocolo sin datos reales | Parcial |
| RN-03 consentimiento previo | #12, #26 | rechazo sin consentimiento y evidencia | Parcial |
| RN-04 credencial revocada | #6, #10 | prueba de rechazo por revocación | Implementado, por verificar E2E |
| RN-05 intentos fallidos | #8, #10 | alerta, bloqueo temporal y auditoría | Parcial |
| RN-06 trámite condicionado | #16, #19, #20 | bloqueo de sesión rechazada | Parcial |
| RN-07 bitácora inmutable | #17 | alteración detectada y acceso restringido | Parcial |
| RN-08 integridad previa a trámite | #15, #16 | documento modificado bloquea trámite | Parcial |
| RN-09 cambio biométrico autorizado | #5, #12 | permiso y evento de aprobación | No iniciada |
| RN-10 vigencia de sesión | #7 | expiración tras diez minutos | No iniciada |

## Cobertura y mantenimiento

- Los RF y RNF prioritarios tienen al menos una issue o una combinación de
  implementación, verificación y evaluación trazable.
- #11 es una decisión explícita, no una brecha silenciosa: RFID físico no
  bloquea QR/MVP.
- #28 debe actualizar esta matriz al cerrar una issue y verificar enlaces,
  evidencia y diferencias entre GitHub y documentación.
