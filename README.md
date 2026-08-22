# proyecto-formatos-01
# Título del proyecto

Aplicación web para la verificación multicapa de identidad y detección de intentos de suplantación en trámites notariales mediante reconocimiento facial, prueba de vida, credenciales QR/RFID y auditoría criptográfica utilizando servicios institucionales simulados


# Nombre referencial del sistema

NotaryVerify – Sistema Experimental de Verificación de Identidad para Trámites Notariales


# Planteamiento del problema

Las notarías intervienen en la formalización de actos y documentos jurídicos en los que la correcta identificación de las personas constituye un elemento fundamental para brindar seguridad a las operaciones realizadas. Una suplantación de identidad puede permitir que una persona intente intervenir en un trámite utilizando la identidad de otra, generando posteriormente consecuencias jurídicas, administrativas y registrales.

La problemática no constituye únicamente un riesgo teórico. En junio de 2026, la Superintendencia Nacional de los Registros Públicos declaró procedente una anotación preventiva notarial sobre una partida del Registro de Predios por una presunta suplantación de identidad relacionada con una escritura pública. Asimismo, durante 2026 se han emitido resoluciones de cancelación de asientos registrales por causales relacionadas con falsificación de documentos, evidenciando que la autenticidad de la identidad y de la documentación continúa siendo un aspecto relevante dentro del entorno notarial y registral peruano (Superintendencia Nacional de los Registros Públicos [Sunarp], 2026a; Sunarp, 2026b).

El sistema registral peruano dispone actualmente de mecanismos oficiales de seguridad. El Sistema de Intermediación Digital de la Sunarp (SID-Sunarp) permite la presentación electrónica de documentos utilizando firma digital y, desde noviembre de 2023, los partes y solicitudes notariales que contienen actos inscribibles deben ser expedidos con firma digital y presentados mediante dicho sistema, de acuerdo con las disposiciones establecidas por Sunarp (Sunarp, 2023).

Por esta razón, el presente proyecto no pretende sustituir al SID-Sunarp, a la firma digital oficial, a Reniec ni a los procedimientos legales utilizados por una notaría. En cambio, se propone investigar y desarrollar una capa tecnológica experimental de verificación previa que permita estudiar cómo diferentes mecanismos electrónicos y biométricos pueden utilizarse conjuntamente para reducir el riesgo de suplantación de identidad antes de continuar con un trámite.

Para ello se propone desarrollar NotaryVerify, una aplicación web que implemente un proceso de verificación multicapa de identidad dentro de un entorno académico controlado.

El funcionamiento del sistema comenzará con el registro de una identidad de prueba. Debido a que el proyecto no contará con acceso a las bases de datos de Reniec ni utilizará información personal real de clientes de una notaría, se desarrollará un servicio denominado “Simulador de Identidad”, que representará de manera académica el comportamiento básico de una consulta institucional.

Este simulador contendrá exclusivamente identidades ficticias creadas para el proyecto. Cada identidad podrá incluir un número de documento ficticio, nombres simulados, fotografía de referencia, estado del registro y otros datos estrictamente necesarios para ejecutar las pruebas.

Cuando sea necesario utilizar reconocimiento facial, las imágenes corresponderán únicamente a integrantes del proyecto o participantes voluntarios que hayan autorizado expresamente su utilización. De esta forma, será posible desarrollar y evaluar el sistema sin utilizar fotografías, documentos ni información biométrica perteneciente a clientes reales de una notaría.

Durante una verificación, el usuario presentará primero una credencial de prueba asociada a la identidad registrada. Esta credencial podrá representarse mediante un código QR o una tarjeta RFID generada específicamente para el prototipo.

La lectura de la credencial no será suficiente para aprobar la identidad. Su función será únicamente recuperar el registro de prueba que corresponde verificar.

Después de identificar el registro esperado, NotaryVerify solicitará una verificación facial mediante cámara. El sistema capturará el rostro presentado y utilizará un modelo local de reconocimiento facial para compararlo con la referencia biométrica previamente registrada.

La implementación podrá utilizar tecnologías de código abierto como OpenCV y modelos compatibles con reconocimiento facial local, evitando depender de servicios comerciales o API biométricas de pago.

Sin embargo, una simple comparación entre dos fotografías presenta el riesgo de que una persona intente engañar al sistema mostrando una fotografía impresa o una imagen desde otro dispositivo. Por este motivo, se incorporará adicionalmente una prueba de vida experimental.

Durante la prueba de vida, el sistema podrá solicitar aleatoriamente acciones como parpadear, girar el rostro hacia una dirección determinada o realizar otro movimiento facial establecido por el prototipo. Estas acciones serán analizadas mediante puntos y características faciales obtenidas desde la cámara.

El carácter aleatorio del desafío permitirá evaluar escenarios en los que un atacante intente utilizar una fotografía estática o material previamente preparado. Este mecanismo será considerado una prueba de vida experimental y no será presentado como sustituto de sistemas biométricos certificados utilizados por instituciones públicas.

El proceso general de verificación será, por tanto:

IDENTIDAD SIMULADA
        ↓
CREDENCIAL QR / RFID
        ↓
REGISTRO ESPERADO
        ↓
CAPTURA FACIAL
        ↓
RECONOCIMIENTO FACIAL
        ↓
PRUEBA DE VIDA
        ↓
REGLAS DE VERIFICACIÓN
        ↓
RESULTADO

El sistema podrá producir resultados como:

IDENTIDAD VERIFICADA
VERIFICACIÓN RECHAZADA
ROSTRO NO COINCIDENTE
PRUEBA DE VIDA FALLIDA
CREDENCIAL NO REGISTRADA
CREDENCIAL REVOCADA
MÚLTIPLES INTENTOS FALLIDOS
VERIFICACIÓN REQUIERE REVISIÓN

Cada resultado deberá almacenarse junto con la fecha, hora, usuario responsable, mecanismo utilizado y resultado obtenido.

Además de validar cada mecanismo de manera independiente, NotaryVerify incorporará un motor de reglas de seguridad. El objetivo será evitar que una única validación sea suficiente para considerar que una identidad fue verificada.

Por ejemplo, una credencial RFID válida no permitirá aprobar una verificación cuando el reconocimiento facial no coincida. De la misma manera, una coincidencia facial no será suficiente cuando el sistema determine que la prueba de vida no ha sido superada.

El prototipo permitirá configurar reglas como:

- Credencial válida + rostro coincidente + prueba de vida correcta = verificación aprobada.
- Credencial válida + rostro diferente = verificación rechazada.
- Credencial válida + fotografía estática detectada durante la prueba = verificación rechazada.
- Credencial inexistente = verificación rechazada.
- Credencial revocada = verificación rechazada.
- Tres o más intentos fallidos consecutivos = generar alerta.
- Cambio de información biométrica = requerir autorización administrativa.

Estas reglas permitirán generar numerosos escenarios controlados de pruebas para evaluar el comportamiento del sistema frente a intentos de suplantación.

Como mecanismo adicional, cada proceso de verificación generará una sesión única. Una sesión contendrá un identificador, la identidad evaluada, los factores utilizados, los resultados obtenidos y la decisión final del sistema.

Una vez que una persona supere la verificación, el sistema podrá asociar dicha sesión con un trámite notarial ficticio. Esto permitirá demostrar posteriormente que, antes de registrar el trámite de prueba, se ejecutó un proceso determinado de comprobación de identidad.

El proyecto también incorporará un mecanismo de integridad documental utilizando SHA-256. Cuando se genere un documento de prueba relacionado con una operación verificada, NotaryVerify calculará una huella criptográfica del archivo.

Si posteriormente el documento es modificado, la huella obtenida será diferente y el sistema podrá informar que el archivo presentado no coincide con la versión originalmente registrada.

Los documentos de prueba podrán incorporar adicionalmente un código QR de verificación que permita consultar información básica sobre su registro y el estado de la verificación realizada, evitando almacenar directamente información personal dentro del código QR.

También se implementará una bitácora de auditoría con encadenamiento criptográfico para las operaciones críticas. Cada evento podrá vincularse criptográficamente con el evento anterior, permitiendo detectar alteraciones realizadas posteriormente en el historial protegido.

De esta manera, el sistema no solamente permitirá responder si una identidad fue aceptada o rechazada, sino también reconstruir qué mecanismos fueron utilizados, qué resultados produjeron y quién realizó la operación.

Como parte de la arquitectura experimental se desarrollarán servicios institucionales simulados. El principal será el Simulador de Identidad, que representará una fuente externa equivalente únicamente para fines académicos a una consulta de información de identidad.

También podrá implementarse un Simulador SID-Sunarp que reciba únicamente aquellos trámites ficticios cuya verificación de identidad haya sido aprobada. Su finalidad no será reproducir todos los procedimientos del SID-Sunarp real, sino permitir probar técnicamente el comportamiento del sistema cuando una aplicación depende de un servicio externo.

Estos simuladores permitirán probar escenarios como:

- identidad existente;
- identidad inexistente;
- fotografía de referencia diferente;
- servicio disponible;
- servicio temporalmente no disponible;
- respuesta incorrecta;
- tiempo de espera agotado;
- trámite autorizado;
- trámite rechazado.

Con ello será posible evaluar no solamente el funcionamiento normal de NotaryVerify, sino también su comportamiento frente a errores de integración y fallos de servicios externos.

El uso de simuladores constituye además una medida de privacidad y seguridad. El nuevo Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales, reconoce los datos biométricos como información sensible, por lo que su tratamiento requiere especiales medidas de protección (Ministerio de Justicia y Derechos Humanos, 2024).

Por esta razón, durante todas las etapas académicas del proyecto se utilizarán identidades ficticias, números de documentos generados específicamente para pruebas, documentos jurídicos simulados y datos biométricos de participantes voluntarios.

La información biométrica utilizada será limitada al propósito académico del proyecto y no se utilizarán fotografías obtenidas desde Internet ni bases de datos reales de ciudadanos.

NotaryVerify tampoco almacenará información biométrica directamente en códigos QR o tarjetas RFID. Estas credenciales contendrán únicamente identificadores o tokens asociados con los registros internos del prototipo.

Las integraciones con Reniec, SID-Sunarp, certificados de firma digital, entidades financieras u otros sistemas gubernamentales no constituirán dependencias obligatorias del proyecto. En lugar de ello, sus interacciones necesarias para los experimentos serán representadas mediante servicios simulados desarrollados por el propio equipo.

Esto permitirá construir escenarios completos de verificación sin requerir credenciales institucionales, acceso a información confidencial o servicios comerciales de pago.

Es importante precisar que NotaryVerify será un prototipo académico y que sus resultados no tendrán valor de identificación legal. Un resultado “IDENTIDAD VERIFICADA” significará únicamente que la persona superó correctamente los mecanismos experimentales configurados dentro del sistema.

La identificación legal continuará correspondiendo a los procedimientos, herramientas y autoridades oficialmente habilitados.

El objetivo principal del proyecto será evaluar si la combinación de múltiples controles —credencial electrónica, reconocimiento facial, prueba de vida, reglas de seguridad, integridad documental y auditoría— permite detectar diferentes escenarios controlados de intento de suplantación con mayor eficacia que el uso aislado de un único mecanismo.

De esta manera, NotaryVerify dejará de estar centrado principalmente en la organización administrativa de expedientes y se enfocará en el problema de la suplantación de identidad, utilizando la trazabilidad documental únicamente como mecanismo complementario para conservar evidencia del proceso de verificación.


# Objetivos del Proyecto


# Objetivo general de investigación

Analizar los riesgos y escenarios de suplantación de identidad que pueden presentarse durante procesos notariales y evaluar mecanismos tecnológicos complementarios de verificación biométrica, prueba de vida, credenciales electrónicas, integridad y auditoría que puedan contribuir a detectar dichos intentos dentro de un entorno académico controlado.


# Objetivos específicos de investigación

1. Identificar y documentar mediante revisión de fuentes y levantamiento de información al menos cinco escenarios potenciales de suplantación o uso indebido de identidad aplicables al contexto de trámites notariales.

2. Analizar los mecanismos actuales de identificación y seguridad utilizados durante los procesos seleccionados de una notaría, diferenciando los controles oficiales de aquellos que puedan ser complementados experimentalmente mediante software.

3. Definir al menos diez reglas de seguridad relacionadas con identidad, credenciales, reconocimiento facial, prueba de vida, intentos fallidos, integridad documental y autorización de operaciones.

4. Analizar los riesgos asociados al tratamiento de información biométrica y personal, definiendo las medidas necesarias para que el 100 % de las pruebas académicas se ejecuten sin utilizar información real de clientes de una notaría.

5. Diseñar un conjunto de escenarios controlados de ataque que incluya como mínimo persona no registrada, rostro incorrecto, fotografía estática, credencial inválida, credencial revocada, documento modificado e intentos consecutivos de verificación.

6. Identificar y priorizar los requerimientos funcionales y no funcionales de NotaryVerify, estableciendo criterios de aceptación verificables para el 100 % de los requerimientos clasificados como de prioridad alta.


# Objetivo de solución


# Objetivo general de solución

Desarrollar y validar un sistema experimental de verificación multicapa de identidad para trámites notariales simulados que combine credenciales electrónicas, reconocimiento facial local, prueba de vida, reglas de seguridad, verificación de integridad y auditoría, utilizando exclusivamente identidades ficticias y datos biométricos autorizados.


# Objetivos específicos de solución

1. Implementar un Simulador de Identidad que permita registrar y consultar identidades ficticias mediante una API propia, incluyendo datos simulados, fotografía de referencia y estado del registro, sin utilizar información procedente de Reniec.

2. Implementar un módulo de enrolamiento biométrico que permita registrar varias muestras faciales de participantes voluntarios y asociarlas exclusivamente con identidades ficticias del proyecto.

3. Implementar un mecanismo de reconocimiento facial local que compare el rostro capturado durante una verificación con la referencia registrada y produzca un resultado de coincidencia acompañado de una métrica de confianza.

4. Implementar una prueba de vida experimental mediante desafíos faciales aleatorios, evaluando acciones como parpadeo o movimientos del rostro antes de permitir continuar con la verificación.

5. Implementar credenciales de prueba mediante QR y RFID, garantizando que su lectura únicamente identifique el registro que debe ser verificado y que la credencial por sí sola no permita aprobar una identidad.

6. Implementar un motor de verificación multicapa que combine los diferentes factores de seguridad y rechace automáticamente los escenarios que incumplan las reglas establecidas.

7. Implementar un mecanismo de detección de intentos repetidos que registre verificaciones fallidas y genere una alerta cuando se supere el límite definido durante el levantamiento de requerimientos.

8. Implementar sesiones de verificación que almacenen el 100 % de los factores utilizados, sus resultados, fecha, hora, usuario responsable y decisión final.

9. Implementar un mecanismo de integridad mediante SHA-256 que detecte correctamente el 100 % de los documentos deliberadamente modificados utilizados durante las pruebas controladas.

10. Implementar códigos QR verificables para los documentos de prueba, rechazando identificadores inexistentes, revocados o asociados con documentos cuya integridad no pueda ser validada.

11. Implementar una bitácora de auditoría con encadenamiento criptográfico que permita detectar durante las pruebas cualquier modificación intencional realizada sobre un evento protegido.

12. Implementar un Simulador SID-Sunarp que permita representar el envío de un trámite ficticio únicamente después de que la sesión de verificación haya sido aprobada, incluyendo escenarios de disponibilidad, rechazo y error del servicio.

13. Evaluar el módulo biométrico mediante al menos 100 intentos controlados distribuidos entre usuarios legítimos y escenarios de suplantación, registrando tasa de aceptación, rechazo, falsos positivos y falsos negativos.

14. Evaluar la prueba de vida mediante escenarios que incluyan como mínimo persona real, fotografía impresa y fotografía mostrada desde una pantalla, documentando los resultados obtenidos y las limitaciones del mecanismo.

15. Implementar controles de acceso basados en roles para que el 100 % de las operaciones críticas de configuración, enrolamiento, modificación y auditoría estén restringidas a usuarios autorizados.

16. Automatizar pruebas unitarias sobre la lógica crítica del sistema, estableciendo como objetivo una cobertura igual o superior al 80 % en los componentes seleccionados.

17. Ejecutar pruebas unitarias, de integración, interfaz, aceptación, exploratorias, seguridad y rendimiento sobre las funcionalidades críticas, manteniendo cero defectos críticos abiertos al momento de la entrega final y trazabilidad entre el 100 % de los requerimientos de prioridad alta y sus respectivos casos de prueba.


# Resultado esperado

Al finalizar el proyecto se espera disponer de un prototipo capaz de representar un proceso completo de intento de verificación de identidad sin utilizar información real de ciudadanos.

Por ejemplo, el sistema contendrá una identidad ficticia denominada PERSONA-001 asociada con un participante voluntario.

El usuario presentará una credencial QR o RFID correspondiente a PERSONA-001. El sistema consultará el Simulador de Identidad y recuperará la referencia correspondiente.

Posteriormente la cámara solicitará una prueba de vida aleatoria y realizará una comparación facial.

Un escenario legítimo podrá producir:

CREDENCIAL: VÁLIDA
IDENTIDAD SIMULADA: ENCONTRADA
PRUEBA DE VIDA: SUPERADA
ROSTRO: COINCIDENTE
RIESGO: BAJO
RESULTADO: IDENTIDAD VERIFICADA

En un escenario de intento de suplantación:

CREDENCIAL: VÁLIDA
IDENTIDAD SIMULADA: ENCONTRADA
PRUEBA DE VIDA: SUPERADA
ROSTRO: NO COINCIDENTE
RESULTADO: VERIFICACIÓN RECHAZADA

También será posible demostrar ataques controlados utilizando fotografías:

CREDENCIAL: VÁLIDA
ROSTRO: DETECTADO
PRUEBA DE VIDA: NO SUPERADA
RESULTADO: POSIBLE INTENTO DE SUPLANTACIÓN

Todos estos eventos quedarán almacenados en una bitácora auditable.

El prototipo permitirá de esta manera experimentar y medir qué tan efectivos resultan los diferentes mecanismos implementados para detectar intentos controlados de suplantación de identidad.


# Referencias

Ministerio de Justicia y Derechos Humanos. (2024). Decreto Supremo N.° 016-2024-JUS: Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales. Gobierno del Perú.
OpenCV. (2026). FaceRecognizerSF. OpenCV Java Documentation.
OpenCV. (2026). OpenCV Zoo: SFace Face Recognition Model.
Google. (2026). MediaPipe Face Landmarker. Google AI for Developers.
Superintendencia Nacional de los Registros Públicos. (2023). Resolución de la Superintendencia Nacional de los Registros Públicos N.° 169-2023-SUNARP/SN. Gobierno del Perú.
Superintendencia Nacional de los Registros Públicos. (2026a). Resolución Jefatural N.° 055-2026-SUNARP/ZRXII/JEF. Gobierno del Perú.
Superintendencia Nacional de los Registros Públicos. (2026b). Resoluciones relacionadas con cancelación de asientos registrales por falsificación documental. Gobierno del Perú.
