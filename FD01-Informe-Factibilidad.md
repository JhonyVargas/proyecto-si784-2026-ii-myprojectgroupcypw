<center>

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *NotaryVerify***

Curso: *Calidad y Pruebas de Software*

Docente: *Patrick Jose Cuadros Quiroga*

Integrantes:

***Cohaila Alvarado, Gabriela Estefania (2022075746)***

***Vargas Luque, Jhony (2022075754)***

**Tacna – Perú**

***2026***

</center>
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

Sistema *NotaryVerify*

Informe de Factibilidad

Versión *1.0*

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|GC, JV|PJCQ|PJCQ|25/08/2026|Versión Original|

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# **INDICE GENERAL**

[1. Descripción del Proyecto](#_Toc52661346)

[2. Riesgos](#_Toc52661347)

[3. Análisis de la Situación actual](#_Toc52661348)

[4. Estudio de Factibilidad](#_Toc52661349)

[4.1 Factibilidad Técnica](#_Toc52661350)

[4.2 Factibilidad económica](#_Toc52661351)

[4.3 Factibilidad Operativa](#_Toc52661352)

[4.4 Factibilidad Legal](#_Toc52661353)

[4.5 Factibilidad Social](#_Toc52661354)

[4.6 Factibilidad Ambiental](#_Toc52661355)

[5. Análisis Financiero](#_Toc52661356)

[6. Conclusiones](#_Toc52661357)

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

**<u>Informe de Factibilidad</u>**

1. <span id="_Toc52661346" class="anchor"></span>**Descripción del Proyecto**

    1.1. Nombre del proyecto

    NotaryVerify – Sistema Experimental de Verificación de Identidad para Trámites Notariales

    1.2. Duración del proyecto

    - Inicio: 25/08/2026
    - Fin: 12/12/2026

    1.3. Descripción

    NotaryVerify es una aplicación web experimental para la verificación multicapa de identidad y la detección de intentos de suplantación en trámites notariales. El sistema combina credenciales electrónicas de prueba (QR/RFID), reconocimiento facial local, prueba de vida, un motor de reglas de seguridad, integridad documental mediante SHA-256 y una bitácora de auditoría con encadenamiento criptográfico.

    El proyecto no pretende sustituir al Sistema de Intermediación Digital de la Sunarp (SID-Sunarp), a la firma digital oficial, a Reniec ni a los procedimientos legales de una notaría. Se plantea como una capa tecnológica académica de verificación previa, desarrollada y evaluada en un entorno controlado, utilizando exclusivamente identidades ficticias y datos biométricos de participantes voluntarios que autoricen expresamente su uso.

    1.4. Objetivos

    1.4.1 Objetivo general

    Desarrollar y evaluar NotaryVerify, un prototipo experimental de verificación multicapa de identidad para trámites notariales que combine credenciales electrónicas, reconocimiento facial local, prueba de vida, reglas de seguridad, integridad documental y auditoría criptográfica, con el fin de analizar su efectividad para detectar intentos controlados de suplantación de identidad.

    1.4.2 Objetivos Específicos

    - Identificar y documentar al menos cinco escenarios de suplantación de identidad aplicables a trámites notariales, mediante revisión de fuentes oficiales (Sunarp, normativa vigente).
    - Implementar un Simulador de Identidad que permita registrar y consultar identidades ficticias mediante una API propia, sin utilizar información real de Reniec.
    - Implementar un módulo de reconocimiento facial local y una prueba de vida experimental (desafíos aleatorios como parpadeo o giro de rostro) mediante OpenCV y MediaPipe.
    - Implementar credenciales de prueba mediante QR y RFID, garantizando que ningún factor evaluado de forma aislada sea suficiente para aprobar una identidad.
    - Implementar un motor de reglas de seguridad multicapa y un mecanismo de integridad documental basado en SHA-256 para detectar documentos modificados.
    - Implementar una bitácora de auditoría con encadenamiento criptográfico que permita detectar alteraciones sobre el historial de operaciones críticas.
    - Evaluar el prototipo mediante al menos 100 intentos controlados de verificación, midiendo tasas de aceptación, rechazo, falsos positivos y falsos negativos, y ejecutar pruebas unitarias, de integración y seguridad con una cobertura mínima del 80 % sobre los componentes críticos.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

2. <span id="_Toc52661347" class="anchor"></span>**Riesgos**

| Riesgo | Probabilidad | Efectos |
| :- | :-: | :-: |
| Cambio excesivo de requerimientos durante el levantamiento de información, originando retrasos en el diseño de las reglas de seguridad | Media | Alto |
| Dificultad para conseguir suficientes participantes voluntarios para las pruebas biométricas | Media | Alto |
| Baja precisión del modelo de reconocimiento facial local ante condiciones variables de iluminación o cámara | Media | Catastrófico |
| Al ser un equipo de solo dos integrantes, la indisponibilidad de uno de ellos origina un retraso significativo | Baja | Catastrófico |
| Limitaciones del hardware disponible (cámara, lector RFID) que afecten la calidad de las pruebas de vida | Media | Alto |
| Manejo inadecuado de datos biométricos de voluntarios que comprometa el cumplimiento de la Ley N.° 29733 | Baja | Catastrófico |

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

3. <span id="_Toc52661348" class="anchor"></span>**Análisis de la Situación actual**

    3.1. Planteamiento del problema

    Las notarías intervienen en la formalización de actos y documentos jurídicos en los que la correcta identificación de las personas constituye un elemento fundamental para brindar seguridad a las operaciones realizadas. Una suplantación de identidad puede permitir que una persona intente intervenir en un trámite utilizando la identidad de otra, generando consecuencias jurídicas, administrativas y registrales.

    La problemática no es únicamente teórica. En junio de 2026, la Superintendencia Nacional de los Registros Públicos declaró procedente una anotación preventiva notarial sobre una partida del Registro de Predios por una presunta suplantación de identidad relacionada con una escritura pública. Durante 2026 también se emitieron resoluciones de cancelación de asientos registrales por causales de falsificación documental, lo que evidencia que la autenticidad de la identidad continúa siendo un aspecto crítico dentro del entorno notarial y registral peruano (Sunarp, 2026a; Sunarp, 2026b).

    El sistema registral peruano ya dispone de mecanismos oficiales de seguridad, como el SID-Sunarp y la firma digital obligatoria para partes notariales desde noviembre de 2023 (Sunarp, 2023). Sin embargo, no existe una capa adicional que combine credenciales electrónicas, biometría facial y prueba de vida como mecanismo experimental de verificación previa dentro de un entorno académico controlado.

    Por ello se propone desarrollar NotaryVerify, utilizando exclusivamente identidades ficticias generadas mediante un "Simulador de Identidad" y datos biométricos de participantes voluntarios, evitando en todo momento el uso de información real de clientes de una notaría.

    3.2. Consideraciones de hardware y software

    **Hardware**

    | Componente | Función |
    | :- | :- |
    | Laptop / PC de desarrollo | Entorno de desarrollo y ejecución del backend, frontend y del módulo de reconocimiento facial durante las pruebas |
    | Cámara web HD | Captura del rostro para el reconocimiento facial y la prueba de vida |
    | Lector/grabador RFID USB | Lectura y grabación de credenciales de prueba tipo RFID |
    | Tarjetas RFID y generador de códigos QR | Generación de credenciales de prueba asociadas a identidades simuladas |

    **Software**

    | Capa | Tecnología | Justificación |
    | :- | :- | :- |
    | Backend / API | Framework web con amplio soporte de librerías (p. ej. Python/FastAPI o Java/Spring Boot) | Permite integrar librerías de reconocimiento facial y construir APIs REST de forma rápida y segura |
    | Reconocimiento facial | OpenCV (FaceRecognizerSF / modelo SFace) | Modelos de código abierto para comparación facial local, sin depender de servicios comerciales de pago |
    | Prueba de vida | MediaPipe Face Landmarker | Detección de puntos faciales para validar acciones aleatorias como parpadeo o giro de rostro |
    | Base de datos | PostgreSQL o Firebase (Firestore) | Almacenamiento de identidades simuladas, sesiones de verificación y bitácora de auditoría |
    | Frontend web | React o Angular | Interfaz web para operadores del prototipo y panel de auditoría |
    | Credenciales | Librerías de generación/lectura de QR y RFID | Generación y lectura de credenciales de prueba (QR/RFID) |
    | Integridad y auditoría | SHA-256 y encadenamiento criptográfico (hash chain) | Verificación de integridad documental y bitácora de auditoría inalterable |

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

4. <span id="_Toc52661349" class="anchor"></span>**Estudio de Factibilidad**

    El presente estudio evalúa la viabilidad técnica, económica, operativa, legal, social y ambiental de desarrollar NotaryVerify como prototipo académico durante el semestre 2026-II, en un entorno controlado y sin uso de información real de clientes de una notaría.

    4.1. <span id="_Toc52661350" class="anchor"></span>Factibilidad Técnica

    | Aspecto | Detalle |
    | :- | :- |
    | Equipos de desarrollo | El equipo cuenta con laptops propias para el desarrollo del backend, frontend y las pruebas del modelo de reconocimiento facial. |
    | Hardware adicional | Se requiere adquirir una cámara web HD y un lector RFID USB, ambos de bajo costo y fácil adquisición local. |
    | Infraestructura de red | Conexión a internet doméstica/universitaria suficiente para el desarrollo y las pruebas; no se requiere infraestructura de red dedicada. |
    | Software y librerías | Se utilizarán exclusivamente herramientas de código abierto (OpenCV, MediaPipe, frameworks web), evitando licencias comerciales o APIs biométricas de pago. |

    4.2. <span id="_Toc52661351" class="anchor"></span>Factibilidad Económica

    4.2.1. Costos Generales

    | Ítem | Cantidad | Costo Unitario (S/.) | Costo Total (S/.) |
    | :- | :-: | :-: | :-: |
    | Lector/grabador RFID USB | 1 | 90.00 | 90.00 |
    | Tarjetas RFID de prueba (paquete x10) | 1 | 30.00 | 30.00 |
    | Cámara web HD 1080p | 1 | 120.00 | 120.00 |
    | Impresión y materiales de documentación | 1 | 50.00 | 50.00 |
    | **Total** | | | **290.00** |

    4.2.2. Costos operativos durante el desarrollo

    | Concepto | Costo Mensual (S/.) | Duración (meses) | Costo Total (S/.) |
    | :- | :-: | :-: | :-: |
    | Dominio web (.com.pe) | 5.83 | 4 | 23.32 |
    | Servicio de generación de códigos QR (API gratuita) | 0.00 | 4 | 0.00 |
    | **Total** | | | **23.32** |

    4.2.3. Costos del ambiente

    | Recurso | Costo Mensual (S/.) | Meses | Costo Total (S/.) |
    | :- | :-: | :-: | :-: |
    | Licencia de entorno de desarrollo (VS Code / PyCharm CE) | 0.00 | 1 | 0.00 |
    | Entorno de pruebas/staging en la nube (plan gratuito + almacenamiento adicional) | 15.00 | 4 | 60.00 |
    | **Total** | | | **60.00** |

    4.2.4. Costos de personal

    | Rol | Costo por hora (S/.) | Horas (5 días) | Sueldo Mensual (S/.) | Meses | Subtotal (S/.) |
    | :- | :-: | :-: | :-: | :-: | :-: |
    | Jefa de Proyecto / Responsable de Calidad y Pruebas — Gabriela Cohaila Alvarado | 13.70 | 4 h | 1,200.00 | 4 | 4,800.00 |
    | Desarrollador Full Stack / Responsable Técnico — Jhony Vargas Luque | 12.50 | 4 h | 1,100.00 | 4 | 4,400.00 |
    | **Total** | | | | | **9,200.00** |

    4.2.5. Costos totales del desarrollo del sistema

    | Categoría | Costo Total (S/.) |
    | :- | :-: |
    | Costos Generales (hardware y equipos) | 290.00 |
    | Costos Operativos (servicios durante el desarrollo) | 23.32 |
    | Costos del Ambiente | 60.00 |
    | Costos de Personal (equipo del proyecto) | 9,200.00 |
    | **Total General** | **9,573.32** |

    4.3. <span id="_Toc52661352" class="anchor"></span>Factibilidad Operativa

    | Aspecto | Descripción | Estado |
    | :- | :- | :-: |
    | Usuarios finales (operadores de prueba) | Estudiantes y voluntarios con conocimientos básicos de informática ejecutarán el flujo de verificación; la interfaz será intuitiva. | viable |
    | Panel de auditoría | Permite consultar sesiones de verificación, resultados y bitácora sin necesidad de conocimientos técnicos avanzados. | viable |
    | Capacitación | Se realizará una sesión breve de inducción a los participantes voluntarios antes de las pruebas biométricas. | planificada |
    | Soporte técnico | El equipo del proyecto brindará soporte durante todo el periodo de pruebas académicas. | planificado |
    | Alcance experimental | El sistema no sustituye a Reniec, SID-Sunarp ni la firma digital oficial; opera únicamente sobre identidades y trámites simulados. | delimitado |

    4.4. <span id="_Toc52661353" class="anchor"></span>Factibilidad Legal

    - **Ley N.° 29733, Ley de Protección de Datos Personales**, y su Reglamento aprobado mediante D.S. N.° 016-2024-JUS: reconocen los datos biométricos como información sensible. El proyecto utilizará exclusivamente identidades ficticias y datos de participantes voluntarios que autoricen expresamente su uso.
    - El proyecto **no sustituye** a Reniec, al SID-Sunarp, a la firma digital oficial (Res. N.° 169-2023-SUNARP/SN) ni a los procedimientos notariales legales vigentes; se plantea como una capa experimental complementaria.
    - **Propiedad intelectual:** el código fuente será propiedad de los integrantes del proyecto para fines académicos.

    4.5. <span id="_Toc52661354" class="anchor"></span>Factibilidad Social

    - Fortalece la confianza en los trámites notariales al reducir el riesgo percibido de suplantación de identidad.
    - **ODS 16 – Paz, Justicia e Instituciones Sólidas:** contribuye a instituciones más transparentes y seguras frente al fraude documental e identitario.
    - **ODS 9 – Industria, Innovación e Infraestructura:** introduce innovación tecnológica (biometría, criptografía) en un proceso tradicionalmente manual.
    - Aporta valor académico como base para investigación futura sobre verificación de identidad aplicada al sector notarial y registral peruano.

    4.6. <span id="_Toc52661355" class="anchor"></span>Factibilidad Ambiental

    - Reduce el uso de papel al digitalizar la verificación y la evidencia, frente a procesos que dependen de copias físicas de documentos.
    - El hardware utilizado (cámara web, lector RFID) tiene un consumo energético bajo.
    - No genera residuos electrónicos significativos, ya que reutiliza equipos existentes de los integrantes del equipo.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

5. <span id="_Toc52661356" class="anchor"></span>**Análisis Financiero**

    Dado que NotaryVerify es un prototipo académico, el presente análisis financiero evalúa un escenario hipotético en el que una notaría adoptara el sistema como capa complementaria de verificación, con el fin de estimar la viabilidad económica de continuar el desarrollo más allá de la etapa experimental.

    5.1. Justificación de la Inversión

    5.1.1. Beneficios del Proyecto

    - Reducción de riesgo legal y reputacional por suplantación de identidad evitada.
    - Reducción del tiempo dedicado a la verificación manual de identidad.
    - Ahorro en gestión documental y auditoría manual de trámites.
    - Aumento de la confianza del cliente y trazabilidad de las operaciones.

    | Tipo | Beneficio | Valor Estimado Mensual (S/.) | Valor Anual (S/.) |
    | :- | :- | :-: | :-: |
    | Tangible | Reducción de riesgo legal y reputacional por suplantación evitada | 250.00 | 3,000.00 |
    | Tangible | Reducción de tiempo de verificación manual de identidad | 150.00 | 1,800.00 |
    | Tangible | Ahorro en gestión documental y auditoría manual | 83.33 | 1,000.00 |
    | **Total** | | **483.33** | **5,800.00** |

    5.1.2. Criterios de Inversión

    5.1.2.1. Relación Beneficio/Costo (B/C)

    | Concepto | Valor (S/.) |
    | :- | :-: |
    | Inversión Total del Proyecto | 9,573.32 |
    | Beneficios Totales (Año 1 + Año 2 + Año 3) | 17,400.00 |
    | Relación B/C | 1.82 → PROYECTO ACEPTADO (B/C > 1) |

    5.1.2.2. Egresos e Ingresos anuales (post-implementación)

    | Gasto | Precio Mensual (S/.) | Cantidad (meses) | Total Anual (S/.) |
    | :- | :-: | :-: | :-: |
    | Mantenimiento del sistema | 50.00 | 12 | 600.00 |
    | Hosting y servicios cloud | 25.00 | 12 | 300.00 |
    | Dominio web (.com.pe) | 5.83 | 12 | 70.00 |
    | Mantenimiento de hardware (lector RFID, cámara) | 20.00 | 12 | 240.00 |
    | **Total de egresos** | | | **1,210.00** |

    El ingreso/beneficio total anual estimado, según la tabla 5.1.1, es de **S/. 5,800.00**.

    5.1.2.3. Valor Actual Neto (VAN)

    | Año | Beneficios (S/.) | Costos Operativos (S/.) | Flujo Neto (S/.) |
    | :- | :-: | :-: | :-: |
    | 0 (Inversión) | 0.00 | 9,573.32 | -9,573.32 |
    | Año 1 | 5,800.00 | 1,210.00 | 4,590.00 |
    | Año 2 | 5,800.00 | 1,210.00 | 4,590.00 |
    | Año 3 | 5,800.00 | 1,210.00 | 4,590.00 |
    | **VAN (COK=12%)** | | | **S/. 1,451.08** |

    Interpretación: el VAN es positivo (S/. 1,451.08 > 0), lo que indica que el proyecto generaría valor por encima del costo de oportunidad del capital bajo el escenario evaluado.

    5.1.2.4. Tasa Interna de Retorno (TIR)

    | Indicador | Valor |
    | :- | :-: |
    | TIR calculada | 20.65 % anual |
    | Costo de Oportunidad del Capital (COK) | 12.00 % anual |
    | Resultado | TIR (20.65 %) > COK (12 %) |

    Interpretación: la TIR supera el costo de oportunidad del capital, por lo que el proyecto resultaría rentable bajo los supuestos del escenario hipotético planteado.

    5.1.3. Proyección del Flujo de Caja

    | Periodo | Ingresos Operativos (S/.) | Egresos (S/.) | Flujo Neto (S/.) |
    | :- | :-: | :-: | :-: |
    | Año 0 | 0.00 | 9,573.32 | -9,573.32 |
    | Año 1 | 5,800.00 | 1,210.00 | 4,590.00 |
    | Año 2 | 5,800.00 | 1,210.00 | 4,590.00 |
    | Año 3 | 5,800.00 | 1,210.00 | 4,590.00 |

    El flujo de caja proyectado muestra que, bajo el escenario hipotético de adopción, la inversión inicial se recuperaría dentro del segundo año de operación.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

6. <span id="_Toc52661357" class="anchor"></span>**Conclusiones**

1. El proyecto es técnicamente **FACTIBLE**: el equipo posee conocimientos en desarrollo web, OpenCV y MediaPipe, y el hardware adicional requerido (cámara web y lector RFID) es de bajo costo y fácil adquisición local.
2. El proyecto es económicamente **VIABLE** bajo el escenario hipotético de adopción evaluado, con una inversión total de S/. 9,573.32 y beneficios anuales estimados de S/. 5,800.00.
3. El sistema puede ser operado por usuarios sin conocimientos técnicos avanzados gracias a su diseño intuitivo; el equipo de dos integrantes brindará soporte durante todo el periodo académico.
4. El proyecto cumple con la Ley N.° 29733 y su Reglamento, al utilizar exclusivamente identidades ficticias y datos biométricos autorizados por voluntarios, sin comprometer información real de clientes de una notaría.
5. NotaryVerify genera valor social al fortalecer la confianza en los trámites notariales y aportar innovación tecnológica alineada con los ODS 9 y 16.
6. El proyecto favorece la reducción del uso de papel y mantiene un consumo energético bajo, sin generar impactos ambientales significativos.
7. Los indicadores financieros del escenario evaluado respaldan la propuesta: B/C = 1.82 (> 1), VAN = S/. 1,451.08 (> 0) y TIR = 20.65 % (> COK 12 %). El proyecto es considerado rentable bajo los supuestos planteados y factible de continuar hacia las siguientes etapas de especificación y arquitectura.

# Referencias

Ministerio de Justicia y Derechos Humanos. (2024). Decreto Supremo N.° 016-2024-JUS: Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales. Gobierno del Perú.
OpenCV. (2026). FaceRecognizerSF. OpenCV Java Documentation.
OpenCV. (2026). OpenCV Zoo: SFace Face Recognition Model.
Google. (2026). MediaPipe Face Landmarker. Google AI for Developers.
Superintendencia Nacional de los Registros Públicos. (2023). Resolución de la Superintendencia Nacional de los Registros Públicos N.° 169-2023-SUNARP/SN. Gobierno del Perú.
Superintendencia Nacional de los Registros Públicos. (2026a). Resolución Jefatural N.° 055-2026-SUNARP/ZRXII/JEF. Gobierno del Perú.
Superintendencia Nacional de los Registros Públicos. (2026b). Resoluciones relacionadas con cancelación de asientos registrales por falsificación documental. Gobierno del Perú.
