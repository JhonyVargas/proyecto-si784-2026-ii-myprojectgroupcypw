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

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|GC, JV|PJCQ|PJCQ|25/08/2026|Versión Original|

Sistema *NotaryVerify*

Documento de Visión

Versión *1.0*

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# **ÍNDICE GENERAL**

[1. Introducción](#_Toc52661346)

1.1. Propósito

1.2. Alcance

1.3. Definiciones, Siglas y Abreviaturas

1.4. Referencias

1.5. Visión General

[2. Posicionamiento](#_Toc52661347)

2.1. Oportunidad de negocio

2.2. Definición del problema

[3. Descripción de los interesados y usuarios](#_Toc52661348)

3.1. Resumen de los interesados

3.2. Resumen de los usuarios

3.3. Entorno de usuario

3.4. Perfiles de los interesados

3.5. Perfiles de los Usuarios

3.6. Necesidades de los interesados y usuarios

[4. Vista General del Producto](#_Toc52661349)

4.1. Perspectiva del producto

4.2. Resumen de capacidades

4.3. Suposiciones y dependencias

4.4. Costos y precios

4.5. Licenciamiento e instalación

[5. Características del producto](#_Toc52661350)

[6. Restricciones](#_Toc52661351)

[7. Rangos de calidad](#_Toc52661352)

[8. Precedencia y Prioridad](#_Toc52661353)

[9. Otros requerimientos del producto](#_Toc52661354)

[10. Conclusiones](#_Toc52661355)

[11. Recomendaciones](#_Toc52661356)

[12. Bibliografía](#_Toc52661357)

[13. Webgrafía](#_Toc52661358)

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

**<u>Informe de Visión</u>**

1. <span id="_Toc52661346" class="anchor"></span>**Introducción**

    1.1. Propósito

    El presente documento de Visión tiene como propósito establecer una definición clara, completa y alineada del sistema NotaryVerify: Sistema Experimental de Verificación de Identidad para Trámites Notariales, desarrollado por el equipo del proyecto como parte del curso Calidad y Pruebas de Software.

    Este documento actúa como el contrato de alto nivel entre los interesados del proyecto (equipo desarrollador, docente del curso, una notaría de referencia considerada de forma hipotética y los participantes voluntarios que aportan datos biométricos de prueba) y el equipo de desarrollo. En él se consolidan los objetivos de investigación y de solución, las necesidades identificadas, el alcance funcional y no funcional, y el posicionamiento de la propuesta frente a la problemática de suplantación de identidad en el entorno notarial peruano.

    La correcta elaboración de este documento garantiza que el equipo comprenda el "qué" y el "porqué" del sistema antes de abordar el "cómo", y sirve como guía para la validación de requerimientos y la medición del éxito del proyecto durante el semestre académico 2026-II.

    1.2. Alcance

    El alcance del proyecto NotaryVerify abarca el desarrollo, implementación y evaluación de un prototipo experimental de verificación multicapa de identidad, operando exclusivamente sobre identidades ficticias y datos biométricos de participantes voluntarios.

    Dentro del alcance del proyecto se considera:

    - Desarrollo de una aplicación web para la ejecución del flujo de verificación (lectura de credencial, captura facial, prueba de vida y resultado).
    - Implementación de un Simulador de Identidad mediante una API propia que registre y consulte identidades ficticias.
    - Implementación de un módulo de reconocimiento facial local (OpenCV) y de prueba de vida experimental (MediaPipe) mediante desafíos aleatorios.
    - Implementación de credenciales de prueba mediante QR y RFID, y de un motor de reglas de seguridad multicapa.
    - Implementación de un mecanismo de integridad documental mediante SHA-256 y de una bitácora de auditoría con encadenamiento criptográfico.
    - Implementación de un Simulador SID-Sunarp que reciba trámites ficticios ya verificados, incluyendo escenarios de error y disponibilidad.

    Fuera del alcance del proyecto se considera:

    - La integración real con Reniec, el SID-Sunarp oficial, la firma digital oficial o cualquier sistema gubernamental de identificación.
    - El uso de información personal o biométrica real de clientes de una notaría.
    - Cualquier valor de identificación legal: los resultados del sistema son exclusivamente experimentales y académicos.
    - La comercialización o despliegue en producción del sistema ante una notaría real.
    - El proyecto se ejecutará entre el 25 de agosto de 2026 y el 12 de diciembre de 2026, con una inversión estimada de S/. 9,573.32, cubierta con recursos propios del equipo.

    1.3. Definiciones, Siglas y Abreviaturas

    | Término | Definición |
    | :- | :- |
    | NotaryVerify | Nombre referencial del sistema objeto del proyecto. |
    | Simulador de Identidad | Servicio desarrollado por el equipo que representa, únicamente con fines académicos, una consulta de información de identidad, utilizando exclusivamente identidades ficticias. |
    | SID-Sunarp | Sistema de Intermediación Digital de la Sunarp; plataforma oficial para la presentación electrónica de documentos notariales con firma digital. |
    | Simulador SID-Sunarp | Servicio experimental que representa el comportamiento del SID-Sunarp únicamente para fines de prueba técnica, sin sustituir al sistema oficial. |
    | Reniec | Registro Nacional de Identificación y Estado Civil. |
    | Prueba de vida (liveness) | Mecanismo que solicita acciones faciales aleatorias (parpadeo, giro de rostro) para verificar que la persona está presente físicamente y no se trata de una fotografía o video. |
    | OpenCV | Biblioteca de código abierto utilizada para el reconocimiento facial local (FaceRecognizerSF / modelo SFace). |
    | MediaPipe Face Landmarker | Herramienta de Google utilizada para la detección de puntos faciales durante la prueba de vida. |
    | SHA-256 | Algoritmo de hash criptográfico utilizado para verificar la integridad de los documentos de prueba. |
    | Encadenamiento criptográfico (hash chain) | Mecanismo que vincula cada evento de la bitácora de auditoría con el evento anterior, permitiendo detectar alteraciones. |
    | QR / RFID | Tecnologías utilizadas para representar credenciales de prueba que identifican el registro a verificar. |
    | Sesión de verificación | Registro único que contiene la identidad evaluada, los factores utilizados, los resultados y la decisión final del sistema. |
    | COK | Costo de Oportunidad del Capital. |
    | VAN | Valor Actual Neto. |
    | TIR | Tasa Interna de Retorno. |
    | MVP | Minimum Viable Product. Versión inicial con las funcionalidades esenciales para validar la propuesta. |

    1.4. Referencias

    Los siguientes documentos han sido utilizados como base para la elaboración de este Documento de Visión:

    - Informe de Factibilidad del Proyecto NotaryVerify – FD01 (Versión 1.0, 2026).

    1.5. Visión General

    NotaryVerify surge como respuesta experimental a la problemática de suplantación de identidad en trámites notariales, evidenciada por resoluciones recientes de la Superintendencia Nacional de los Registros Públicos. La solución combina una aplicación web, un Simulador de Identidad, credenciales de prueba QR/RFID, reconocimiento facial local, prueba de vida, un motor de reglas de seguridad multicapa, integridad documental mediante SHA-256 y una bitácora de auditoría con encadenamiento criptográfico. Su visión es demostrar, dentro de un entorno académico controlado, si la combinación de múltiples controles permite detectar intentos de suplantación con mayor eficacia que el uso aislado de un único mecanismo, sentando una base para investigación futura aplicada al sector notarial y registral peruano.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

2. <span id="_Toc52661347" class="anchor"></span>**Posicionamiento**

    2.1. Oportunidad de negocio

    NotaryVerify se posiciona como una propuesta de investigación aplicada, no como un producto comercial listo para su venta. Su oportunidad radica en la brecha existente entre los mecanismos oficiales de seguridad ya disponibles (SID-Sunarp, firma digital obligatoria desde 2023) y la ausencia de una capa adicional de verificación biométrica previa que pueda complementar dichos mecanismos dentro de una notaría.

    | Problema identificado | Impacto | Oportunidad |
    | :- | :- | :- |
    | Ausencia de una verificación biométrica previa en trámites notariales | Riesgo de suplantación de identidad no detectado a tiempo, con consecuencias jurídicas y registrales (casos Sunarp 2026) | Capa experimental de verificación multicapa (credencial + biometría + prueba de vida) |
    | Validación basada únicamente en el documento físico presentado | Un documento válido no garantiza que la persona presente sea su titular | Comparación facial local frente a una referencia biométrica registrada |
    | Falta de trazabilidad de las verificaciones realizadas | Dificultad para reconstruir qué controles se aplicaron ante un caso de suplantación | Bitácora de auditoría con encadenamiento criptográfico |
    | Dependencia de un único factor para aprobar una identidad | Un solo mecanismo comprometido (p. ej. una fotografía) puede habilitar el fraude | Motor de reglas que exige múltiples factores aprobados simultáneamente |

    La propuesta se apoya en tres consideraciones:

    - **Vacío experimental identificado:** no se ha encontrado evidencia pública de una capa de verificación biométrica multicapa aplicada específicamente a trámites notariales en el contexto peruano.
    - **Base normativa vigente:** la Ley N.° 29733 y su Reglamento (D.S. N.° 016-2024-JUS) reconocen los datos biométricos como información sensible, lo que refuerza la necesidad de estudiar mecanismos de verificación que respeten dicho marco.
    - **Continuidad académica:** los resultados del prototipo pueden servir como base para investigaciones posteriores o para una eventual propuesta piloto ante una notaría real, una vez validado el enfoque experimental.

    2.2. Definición del problema

    Las notarías intervienen en la formalización de actos y documentos jurídicos en los que la correcta identificación de las personas es un elemento fundamental. Una suplantación de identidad puede permitir que una persona intervenga en un trámite utilizando la identidad de otra, generando consecuencias jurídicas, administrativas y registrales. En junio de 2026, la Sunarp declaró procedente una anotación preventiva notarial por presunta suplantación de identidad relacionada con una escritura pública, y durante el mismo año se emitieron resoluciones de cancelación de asientos registrales por falsificación documental (Sunarp, 2026a; Sunarp, 2026b). Actualmente no existe evidencia de que las notarías empleen, además de los mecanismos oficiales de firma digital y el SID-Sunarp, una capa adicional de verificación biométrica y de prueba de vida como control experimental previo al trámite.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

3. <span id="_Toc52661348" class="anchor"></span>**Descripción de los interesados y usuarios**

    3.1. Resumen de los interesados

    | Interesado | Rol | Expectativas principales |
    | :- | :- | :- |
    | Docente del curso (Patrick Cuadros Quiroga) | Evaluador académico | Verificar el cumplimiento de los objetivos de investigación y de solución, y la aplicación correcta de prácticas de calidad y pruebas de software. |
    | Equipo del proyecto (Gabriela Cohaila, Jhony Vargas) | Investigadores / desarrolladores | Entregar un prototipo funcional que permita evaluar la efectividad de la verificación multicapa frente a escenarios controlados de suplantación. |
    | Notaría de referencia (entorno hipotético) | Beneficiario potencial | Contar con evidencia experimental de que la propuesta puede reducir el riesgo de suplantación de identidad en sus trámites. |
    | Participantes voluntarios | Fuente de datos biométricos de prueba | Que su información biométrica se utilice exclusivamente con fines académicos, bajo consentimiento expreso y sin difusión pública. |

    3.2. Resumen de los usuarios

    | Usuario | Descripción | Frecuencia de uso |
    | :- | :- | :- |
    | Operador de verificación | Persona que ejecuta el flujo de verificación (lectura de credencial, captura facial, prueba de vida). | Uso frecuente durante las sesiones de prueba controladas. |
    | Administrador / Auditor | Supervisa sesiones de verificación, configura reglas de seguridad y revisa la bitácora de auditoría. | Uso periódico. |
    | Participante voluntario (identidad simulada) | Persona cuyo rostro se registra como referencia biométrica de una identidad ficticia y que participa en los intentos de verificación. | Uso puntual (enrolamiento y verificación). |

    3.3. Entorno de usuario

    - **Operador de verificación**
      - Integrante del equipo o voluntario capacitado, edad 20-30 años.
      - Manejo básico de aplicaciones web y de una cámara.
      - Necesidad: flujo lineal y claro (credencial → captura facial → prueba de vida → resultado), con mensajes de error comprensibles.
    - **Administrador / Auditor**
      - Integrante del equipo con conocimientos técnicos, responsable de revisar reglas y bitácora.
      - Necesidad: panel con historial de sesiones, resultados y trazabilidad de eventos.
    - **Participante voluntario**
      - Estudiantes u otras personas que autorizan expresamente el uso de su rostro para una identidad ficticia.
      - Necesidad: proceso de enrolamiento breve, con explicación clara del uso que se dará a su información.

    3.4. Perfiles de los interesados

    - **Docente del curso**
      - Responsable de aprobar los entregables académicos del proyecto (FD01 a FD06).
      - Expectativa: trazabilidad entre requerimientos, pruebas y resultados obtenidos.
      - Restricción: el proyecto debe cumplir con el cronograma del semestre 2026-II.
    - **Equipo del proyecto**
      - Integrantes: Gabriela Cohaila Alvarado (Jefa de Proyecto / Responsable de Calidad y Pruebas) y Jhony Vargas Luque (Desarrollador Full Stack / Responsable Técnico).
      - Expectativa: entregar un prototipo funcional dentro del plazo (25/08/2026 – 12/12/2026) que sustente los objetivos de investigación planteados.
      - Restricción: equipo de solo dos integrantes, con recursos propios limitados y dependencia de la disponibilidad de participantes voluntarios.

    3.5. Perfiles de los Usuarios

    | Perfil | Conocimientos requeridos | Interacción típica |
    | :- | :- | :- |
    | Operador de verificación | Manejo básico de un navegador web y de una cámara. | Presenta la credencial de prueba (QR/RFID), realiza la captura facial y ejecuta la prueba de vida solicitada por el sistema. |
    | Administrador / Auditor | Manejo de aplicaciones web y comprensión de reglas de seguridad. | Configura reglas del motor de verificación, revisa sesiones registradas y consulta la bitácora de auditoría. |
    | Participante voluntario | Ninguno específico; solo disposición a participar en las pruebas. | Autoriza el uso de su rostro, participa en el enrolamiento y en los intentos de verificación controlados. |

    3.6. Necesidades de los interesados y usuarios

    | Necesidad | Prioridad |
    | :- | :-: |
    | Verificar la identidad mediante múltiples factores, sin depender de uno solo. | Alta |
    | Detectar intentos de suplantación mediante fotografías o material estático (prueba de vida). | Alta |
    | Registrar de forma trazable cada sesión de verificación (factores, resultados, responsable). | Alta |
    | Garantizar la integridad de los documentos generados durante una operación verificada. | Alta |
    | Proteger los datos biométricos de los participantes conforme a la Ley N.° 29733. | Alta |
    | Disponer de un panel de auditoría para revisar el historial de verificaciones. | Media |

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

4. <span id="_Toc52661349" class="anchor"></span>**Vista General del Producto**

    4.1. Perspectiva del producto

    NotaryVerify es un producto experimental autónomo que no depende de sistemas preexistentes en una notaría real. No reemplaza a Reniec, al SID-Sunarp ni a la firma digital oficial; en su lugar, se integra con servicios institucionales simulados desarrollados por el propio equipo: el Simulador de Identidad y el Simulador SID-Sunarp. El módulo de reconocimiento facial y de prueba de vida se ejecuta de forma local (OpenCV, MediaPipe), y los resultados de cada sesión se almacenan junto con la bitácora de auditoría con encadenamiento criptográfico, garantizando consistencia entre el flujo de verificación y el panel de auditoría.

    4.2. Resumen de capacidades

    - Registro y consulta de identidades ficticias mediante el Simulador de Identidad.
    - Lectura de credenciales de prueba (QR/RFID) que identifican el registro a verificar.
    - Reconocimiento facial local mediante OpenCV, con métrica de confianza.
    - Prueba de vida experimental mediante desafíos aleatorios (MediaPipe Face Landmarker).
    - Motor de reglas de seguridad multicapa que combina los factores evaluados.
    - Verificación de integridad documental mediante SHA-256 y códigos QR de verificación.
    - Bitácora de auditoría con encadenamiento criptográfico para operaciones críticas.
    - Simulador SID-Sunarp para representar el envío de trámites ficticios ya verificados.

    4.3. Suposiciones y dependencias

    - El equipo cuenta con laptops propias con cámara web compatible para las pruebas de reconocimiento facial.
    - Se dispone de un lector/grabador RFID USB y de tarjetas de prueba compatibles.
    - Las librerías OpenCV y MediaPipe son compatibles con el hardware disponible del equipo.
    - Se cuenta con la disponibilidad de al menos un grupo de participantes voluntarios que autoricen el uso de su rostro para las pruebas biométricas.

    4.4. Costos y precios

    Los costos del proyecto NotaryVerify han sido determinados a partir del estudio de factibilidad económica (Informe FD01, Versión 1.0, 2026). La inversión total contempla costos generales de hardware, costos operativos durante el desarrollo, costos del ambiente de pruebas y costos de personal del equipo del proyecto.

    | Categoría | Total (S/.) |
    | :- | -: |
    | Costos Generales (hardware y equipos) | 290.00 |
    | Costos Operativos (servicios durante el desarrollo) | 23.32 |
    | Costos del Ambiente (entorno de pruebas / staging) | 60.00 |
    | Costos de Personal (equipo del proyecto) | 9,200.00 |
    | **Total General** | **9,573.32** |

    4.5. Licenciamiento e instalación

    El código fuente de NotaryVerify será propiedad de los integrantes del equipo para fines académicos, documentado adecuadamente para su continuidad en cursos posteriores o como base de futuras investigaciones. La instalación contempla: configuración del entorno local de desarrollo, despliegue de una versión de demostración en un entorno de pruebas/staging, y conexión del hardware de prueba (cámara web y lector RFID). No se contempla distribución comercial ni instalación en la infraestructura de una notaría real.

5. <span id="_Toc52661350" class="anchor"></span>**Características del producto**

    **MUST (Indispensables)**

    - Simulador de Identidad accesible mediante una API propia, con registro y consulta de identidades ficticias.
    - Módulo de reconocimiento facial local con métrica de confianza de coincidencia.
    - Prueba de vida experimental mediante desafíos aleatorios.
    - Lectura de credenciales de prueba QR y RFID, sin que ningún factor apruebe una identidad por sí solo.
    - Motor de reglas de seguridad multicapa que combine credencial, rostro y prueba de vida.
    - Registro completo de sesiones de verificación (factores, resultados, fecha, hora, responsable).

    **SHOULD (Importantes)**

    - Verificación de integridad documental mediante SHA-256.
    - Códigos QR de verificación en los documentos de prueba generados.
    - Bitácora de auditoría con encadenamiento criptográfico.
    - Panel de supervisión/auditoría para consultar el historial de verificaciones.

    **COULD (Opcionales)**

    - Simulador SID-Sunarp para representar el envío de trámites ficticios ya verificados.
    - Controles de acceso basados en roles para operaciones críticas de configuración.
    - Mecanismo de alerta ante intentos consecutivos fallidos de verificación.

6. <span id="_Toc52661351" class="anchor"></span>**Restricciones**

    - El proyecto debe ejecutarse entre el 25 de agosto de 2026 y el 12 de diciembre de 2026, con una inversión que no exceda S/. 9,573.32.
    - El sistema debe operar exclusivamente con identidades ficticias y datos biométricos de participantes voluntarios que autoricen expresamente su uso; no se utilizará información real de clientes de una notaría.
    - El hardware adicional debe limitarse a componentes de bajo costo y fácil adquisición local (cámara web, lector RFID USB).
    - El equipo del proyecto está conformado únicamente por dos integrantes, lo que condiciona el alcance funcional que puede completarse dentro del semestre.
    - El sistema no tendrá valor de identificación legal ni sustituirá a Reniec, al SID-Sunarp ni a la firma digital oficial.

7. <span id="_Toc52661352" class="anchor"></span>**Rangos de calidad**

    - El módulo biométrico debe evaluarse mediante al menos 100 intentos controlados, registrando tasas de aceptación, rechazo, falsos positivos y falsos negativos.
    - La cobertura de pruebas automatizadas sobre la lógica crítica del sistema debe ser igual o superior al 80 %.
    - El sistema debe mantener cero defectos críticos abiertos al momento de la entrega final, con trazabilidad entre el 100 % de los requerimientos de prioridad alta y sus casos de prueba.
    - La bitácora de auditoría debe detectar el 100 % de las alteraciones deliberadas introducidas durante las pruebas controladas sobre el historial protegido.
    - El mecanismo de integridad SHA-256 debe detectar el 100 % de los documentos de prueba deliberadamente modificados.

8. <span id="_Toc52661353" class="anchor"></span>**Precedencia y Prioridad**

    Los requerimientos del producto se priorizan utilizando el método MoSCoW. Tienen máxima prioridad (MUST) las funcionalidades núcleo del flujo experimental: Simulador de Identidad, reconocimiento facial, prueba de vida, credenciales de prueba y el motor de reglas multicapa, ya que sin ellas no es posible evaluar la hipótesis central del proyecto. La integridad documental y la bitácora de auditoría se ubican en el segundo nivel (SHOULD), al ser mecanismos complementarios de trazabilidad. El Simulador SID-Sunarp, los controles de acceso por rol y las alertas por intentos fallidos se consideran complementarios (COULD) y se evaluarán en función del tiempo disponible durante el semestre.

9. <span id="_Toc52661354" class="anchor"></span>**Otros requerimientos del producto**

    a) Estándares legales

    - **Ley N.° 29733 – Ley de Protección de Datos Personales** y su Reglamento (D.S. N.° 016-2024-JUS): los datos biométricos son tratados como información sensible; el proyecto utilizará exclusivamente identidades ficticias y datos de voluntarios con autorización expresa.
    - El proyecto **no sustituye** a Reniec, al SID-Sunarp (Res. N.° 169-2023-SUNARP/SN) ni a la firma digital oficial; sus resultados no tienen valor de identificación legal.
    - Propiedad intelectual: el código fuente será propiedad de los integrantes del proyecto para fines académicos.

    b) Estándares de comunicación

    - Comunicación entre el frontend web y las APIs del Simulador de Identidad / Simulador SID-Sunarp: protocolo HTTPS (TLS 1.2 o superior) sobre una API REST.
    - Lectura de credenciales RFID: estándar ISO/IEC 14443 (tarjetas de proximidad de uso común en lectores USB comerciales).
    - Generación y lectura de credenciales QR: codificación estándar QR (ISO/IEC 18004).

    c) Estándares de cumplimiento de la plataforma

    - Aplicación web con diseño responsive, compatible con los navegadores más utilizados (Chrome, Edge, Firefox).
    - Lineamientos básicos de accesibilidad (WCAG 2.1) para el panel de operación y el panel de auditoría.

    d) Estándares de calidad y seguridad

    Calidad:

    - Aplicación de ISO/IEC 25010 para evaluar funcionalidad, eficiencia, usabilidad, fiabilidad, mantenibilidad y seguridad del prototipo.
    - Gestión del código fuente mediante Git, con revisión antes de integrar cambios a la rama principal.
    - Pruebas unitarias, de integración, de interfaz, de aceptación, exploratorias, de seguridad y de rendimiento sobre las funcionalidades críticas.

    Seguridad:

    - Los datos biométricos de los participantes se almacenarán únicamente como referencias necesarias para la comparación (no se publicarán ni compartirán fuera del entorno académico del proyecto).
    - Cifrado de datos en tránsito mediante HTTPS/TLS.
    - Principio de mínimo privilegio para los roles de operador y administrador/auditor.
    - Encadenamiento criptográfico de la bitácora de auditoría para detectar alteraciones sobre eventos ya registrados.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

10. <span id="_Toc52661355" class="anchor"></span>**Conclusiones**

NotaryVerify constituye una propuesta experimental viable para estudiar, dentro de un entorno académico controlado, si la combinación de credenciales electrónicas, reconocimiento facial local, prueba de vida, reglas de seguridad multicapa, integridad documental y auditoría criptográfica permite detectar con mayor eficacia los intentos de suplantación de identidad en trámites notariales, frente al uso aislado de un único mecanismo. El análisis de factibilidad (FD01) respalda la viabilidad técnica y económica del proyecto bajo un escenario hipotético de adopción (B/C = 1.82, VAN = S/. 1,451.08, TIR = 20.65 % > COK 12 %), mientras que el presente documento de Visión delimita con claridad que se trata de un prototipo académico, sin valor de identificación legal, que utiliza exclusivamente identidades ficticias y datos biométricos autorizados por participantes voluntarios.

11. <span id="_Toc52661356" class="anchor"></span>**Recomendaciones**

- Iniciar el reclutamiento de participantes voluntarios desde las primeras semanas del proyecto, dado que la disponibilidad de datos biométricos de prueba es una dependencia crítica identificada en los riesgos del FD01.
- Documentar de forma explícita el proceso de consentimiento informado para el uso del rostro de cada participante voluntario, antes de iniciar cualquier prueba biométrica.
- Ejecutar pruebas tempranas del módulo de reconocimiento facial y prueba de vida en distintas condiciones de iluminación, dado que es uno de los riesgos técnicos de mayor impacto identificados.
- Mantener comunicación periódica con el docente del curso para validar el avance frente a los objetivos de investigación y de solución planteados.

12. <span id="_Toc52661357" class="anchor"></span>**Bibliografía**

Ministerio de Justicia y Derechos Humanos. (2024). Decreto Supremo N.° 016-2024-JUS: Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales. Gobierno del Perú.

Superintendencia Nacional de los Registros Públicos. (2023). Resolución de la Superintendencia Nacional de los Registros Públicos N.° 169-2023-SUNARP/SN. Gobierno del Perú.

Superintendencia Nacional de los Registros Públicos. (2026a). Resolución Jefatural N.° 055-2026-SUNARP/ZRXII/JEF. Gobierno del Perú.

Superintendencia Nacional de los Registros Públicos. (2026b). Resoluciones relacionadas con cancelación de asientos registrales por falsificación documental. Gobierno del Perú.

Sommerville, I. (2016). Ingeniería de Software (10a ed.). Pearson Educación.

ISO/IEC. (2011). ISO/IEC 25010:2011 - Systems and software engineering - SQuaRE.

13. <span id="_Toc52661358" class="anchor"></span>**Webgrafía**

Documentación oficial de OpenCV: https://docs.opencv.org/

Documentación oficial de MediaPipe: https://developers.google.com/mediapipe
