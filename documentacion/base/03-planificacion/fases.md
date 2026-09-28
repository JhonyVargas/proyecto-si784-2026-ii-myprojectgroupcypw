# Fases y definición de salida

## MVP

El MVP no es solo una pantalla: debe demostrar, con identidad ficticia y
participante consentido, credencial válida, rostro coincidente, prueba de vida
superada, reglas y resultado almacenado. Incluye rechazos por credencial
inexistente, rostro no coincidente y prueba de vida fallida. Su ruta crítica es
[#4](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/4)
→ [#5](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/5)
→ [#6](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/6)
→ [#7](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/7)
→ [#8](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/8)
→ [#9](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/9)
→ [#10](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/10).

## V1

V1 amplía el MVP sin reemplazar sus tecnologías locales: RFID simulado y
decisión de hardware (#11), aprobación de biometría (#12), reglas configurables
(#13), liveness/rostro reproducibles (#14, #18), evidencia documental y
auditoría (#15–#17), SID resiliente (#19–#20) y operación/CI (#21–#25).

## Evaluación experimental

La evaluación no completa automáticamente una feature. Las issues #26 y #27
ejecutan protocolos y reportan métricas agregadas; #28 comprueba que cada
requisito prioritario tenga una relación verificable con implementación,
prueba o evidencia. Todo uso biométrico requiere consentimiento voluntario.

## Entrega final

La issue #29 consolida demostración, documentación, riesgos y criterios de
salida. No puede cerrar si quedan defectos críticos o si GitHub, evidencia y
documentación discrepan.

## Posterior al alcance actual

La decisión de #11 difiere la integración RFID física: no hay hardware en esta
etapa y el proyecto usa un adaptador simulado con UID hexadecimal canónico. Un
lector futuro deberá implementar el puerto definido sin cambiar reglas ni el
contrato QR. No se planifican servicios institucionales reales, identificación
legal ni datos biométricos de terceros.
