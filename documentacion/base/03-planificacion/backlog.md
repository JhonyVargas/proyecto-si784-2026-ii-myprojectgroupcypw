# Backlog priorizado y estado real

Las issues de GitHub contienen el alcance ejecutable completo. El estado actual
del producto se audita contra código y pruebas; `parcial` no significa que una
feature esté lista para cerrar.

## Críticas para el MVP

| Issue | Brecha observada | Estado base |
| --- | --- | --- |
| [#4](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/4) | Autenticación de operadores y administradores. | Cerrada y verificada |
| [#5](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/5) | Autorización API/UI por rol. | Cerrada y verificada |
| [#6](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/6) | Contrato y errores HTTP del flujo existente. | Cerrada y verificada |
| [#7](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/7) | Vigencia, responsable, historial y filtros de sesión. | Cerrada y verificada |
| [#8](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/8) | Alerta y bloqueo temporal tras fallos. | Cerrada y verificada |
| [#9](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/9) | Estados de operador y errores de interfaz. | Cerrada y verificada |
| [#10](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/10) | Evidencia automatizada de cuatro escenarios MVP. | Cerrada y verificada |

## V1 y endurecimiento académico

[#11](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/11) RFID simulado/decisión de hardware;
[#12](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/12) cambio biométrico autorizado;
[#13](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/13) reglas configurables;
[#14](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/14) liveness experimental;
[#15](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/15) QR documental;
[#16](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/16) evidencia integrada;
[#17](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/17) auditoría;
[#18](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/18) confianza facial;
[#19](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/19) SID resiliente;
[#20](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/20) UI de trámite;
[#21](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/21) persistencia;
[#22](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/22) privacidad;
[#23](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/23) CI;
[#24](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/24) rendimiento; y
[#25](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/25) compatibilidad/observabilidad.

## Evaluación y cierre

[#26](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/26) evaluación facial;
[#27](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/27) evaluación de liveness;
[#28](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/28) trazabilidad; y
[#29](https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-ii-myprojectgroupcypw/issues/29) entrega final.

## Estado M1

Las issues #4 a #10 están cerradas y su evidencia está versionada. La ruta
crítica MVP fue #4 → #5 → #7 → #8 → #9 → #10; #6 fue un cimiento paralelo
cerrado antes de #7. El siguiente trabajo elegible pertenece a M2 y no forma
parte del cierre de este milestone.

## Estado M2

Las issues #11 y #12 están implementadas con evidencia versionada. La decisión
de #11 es explícita: no hay hardware RFID en esta etapa; el adaptador simulado
usa UID hexadecimal en mayúsculas sin separadores y una integración física se
difirió. El criterio de salida M2 queda cubierto sin alterar el QR del MVP.

## Estado M3

Las issues #18 y #14 están implementadas: la comparación facial tiene
preprocesamiento, umbral técnico y errores normalizados; la prueba de vida usa
un desafío temporal emitido por el servidor y negativos controlados. Ambas usan
evidencia sintética sin red y no afirman precisión/FPR ni resistencia
certificada. La issue #13 completa las reglas configurables y permanece en la
ruta crítica de M3.
