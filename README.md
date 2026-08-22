# proyecto-formatos-01
# Título del proyecto 
Aplicación web para la trazabilidad y verificación de integridad de expedientes notariales mediante RFID, QR, reconocimiento facial y auditoría criptográfica en una notaría de Tacna
# Nombre referencial del sistema: 
NotaryTrace

# Planteamiento del problema
Las notarías cumplen una función importante en la formalización de documentos jurídicos, por lo que requieren mecanismos que garanticen la correcta identificación de las personas, conservación de documentos, trazabilidad de expedientes y detección de alteraciones. En el Perú, casos recientes de falsificación documental y suplantación de identidad evidencian que estos riesgos continúan presentes. Al mismo tiempo, herramientas oficiales como SID-Sunarp ya permiten la presentación electrónica de documentos con firma digital, por lo que cualquier nueva solución debe complementar y no reemplazar estos sistemas.

Ante esta situación, se propone NotaryTrace, una aplicación web orientada a mejorar la gestión y trazabilidad física y digital de expedientes notariales. Antes de su desarrollo se realizará un levantamiento de información en una notaría de Tacna para conocer sus procesos actuales, herramientas utilizadas y posibles dificultades relacionadas con localización, seguimiento, seguridad y generación de reportes.

El sistema permitirá registrar expedientes mediante identificadores únicos, estados, responsables, fechas e historial de operaciones. También integrará un prototipo con RFID y ESP32 para identificar y registrar movimientos de expedientes físicos, así como mecanismos de verificación documental mediante SHA-256 y códigos QR para detectar modificaciones y consultar información pública básica de los documentos.

Además, incorporará una bitácora de auditoría con encadenamiento criptográfico para detectar alteraciones en el historial y un módulo experimental de reconocimiento facial con OpenCV, utilizado únicamente con participantes voluntarios y con fines académicos. Este componente no reemplazará los mecanismos oficiales de identificación ni se conectará con Reniec.

Para proteger la privacidad, el proyecto utilizará expedientes ficticios, documentos de prueba e identidades simuladas. Tampoco dependerá de integraciones oficiales con Reniec, SID-Sunarp, firmas digitales, bancos u otros servicios externos, pudiendo utilizar simulaciones cuando sea necesario.

En conjunto, NotaryTrace integrará gestión de expedientes, trazabilidad, RFID, QR, SHA-256, reconocimiento facial, auditoría y reportes en una sola solución, manteniendo un alcance viable para ser desarrollado y evaluado durante un semestre académico.

# Objetivos del Proyecto

# Objetivo general
Desarrollar y validar una aplicación web integrada con componentes electrónicos que permita gestionar la trazabilidad física y digital de expedientes notariales, verificar la integridad de documentos y evaluar mecanismos complementarios de identificación y auditoría dentro de un entorno académico controlado.

# Objetivos específicos

Identificar y documentar como mínimo cuatro etapas críticas del ciclo de atención de los expedientes notariales seleccionados, mediante entrevistas y levantamiento de información con al menos un representante o trabajador de una notaría de Tacna que conozca el proceso estudiado.
Identificar el 100 % de los actores involucrados en los procesos seleccionados para el proyecto, estableciendo las operaciones, responsabilidades y niveles de acceso correspondientes a cada perfil.
Documentar al menos diez reglas de negocio relacionadas con estados, responsables, movimientos, verificación, documentos y seguridad, validándolas con la persona designada por la notaría antes de incorporarlas a la solución.
Identificar las principales dificultades relacionadas con trazabilidad, localización de expedientes, integridad documental, identificación y generación de información administrativa, clasificándolas según frecuencia, impacto y posibilidad de ser atendidas mediante software.
Definir y priorizar los requerimientos funcionales y no funcionales del sistema, estableciendo criterios de aceptación verificables para el 100 % de los requerimientos considerados de prioridad alta.
Analizar los riesgos asociados al tratamiento de información personal y biométrica, identificando las medidas que deberán aplicarse para desarrollar y probar el prototipo sin utilizar datos reales de clientes de la notaría.

# Objetivo Solucion
# Objetivo general de solución
Desarrollar y validar una aplicación web integrada con componentes electrónicos que permita gestionar la trazabilidad física y digital de expedientes notariales, verificar la integridad de documentos y evaluar mecanismos complementarios de identificación y auditoría dentro de un entorno académico controlado.

# Objetivos específicos de solución
Implementar un módulo de gestión de expedientes que permita registrar el 100 % de los datos obligatorios definidos durante el levantamiento de requerimientos y generar automáticamente un código único para cada expediente.
Implementar un flujo controlado de estados que registre cada transición realizada sobre un expediente y rechace el 100 % de las transiciones que hayan sido definidas como inválidas por las reglas de negocio seleccionadas.
Implementar un historial de trazabilidad que registre para el 100 % de las operaciones críticas el expediente involucrado, usuario responsable, estado anterior, estado posterior, fecha y hora de la operación.
Implementar un prototipo electrónico RFID utilizando ESP32 y un lector compatible, asociando cada etiqueta de prueba con un expediente y consiguiendo al menos un 95 % de lecturas procesadas correctamente durante un conjunto mínimo de 50 pruebas controladas.
Implementar un mecanismo de integridad documental mediante SHA-256 que genere una huella única para los documentos registrados y detecte correctamente el 100 % de los archivos deliberadamente modificados utilizados durante las pruebas de integridad.
Implementar códigos QR verificables para los documentos seleccionados, de manera que el 100 % de los códigos válidos utilizados en las pruebas redirijan al registro correspondiente y que los identificadores inexistentes o anulados sean rechazados por el sistema.
Implementar una bitácora de auditoría con encadenamiento criptográfico que permita verificar la consistencia de las operaciones críticas almacenadas e identificar durante las pruebas cualquier alteración intencional realizada sobre los registros protegidos.
Implementar un módulo experimental de reconocimiento facial local utilizando únicamente información biométrica de participantes voluntarios, evaluándolo mediante un mínimo de 50 intentos controlados y obteniendo como objetivo una tasa de identificación correcta igual o superior al 90 % bajo las condiciones establecidas para el prototipo.
Implementar controles de acceso basados en roles, garantizando mediante pruebas que el 100 % de las funcionalidades críticas seleccionadas únicamente puedan ser ejecutadas por los perfiles autorizados.
Implementar un panel de seguimiento y reportes que permita consultar expedientes por código, estado, responsable, tipo y fecha, así como visualizar indicadores relacionados con expedientes activos, finalizados, observados y tiempos registrados entre etapas.
Automatizar las pruebas de la lógica de negocio crítica, estableciendo como objetivo alcanzar una cobertura igual o superior al 80 % sobre los componentes seleccionados para pruebas unitarias.
Ejecutar pruebas unitarias, de integración, interfaz, aceptación, seguridad y rendimiento sobre las funcionalidades críticas, logrando que el proyecto finalice sin defectos críticos abiertos y con trazabilidad entre el 100 % de los requerimientos de prioridad alta y sus respectivos casos de prueba.




# Referencias
Ministerio de Justicia y Derechos Humanos. (2024). Decreto Supremo N.° 016-2024-JUS: Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales. Gobierno del Perú.
OpenCV. (2026). OpenCV: Open Source Computer Vision Library. Open Source Vision Foundation.
Superintendencia Nacional de los Registros Públicos. (2022). Resolución de la Superintendencia Nacional de los Registros Públicos N.° 005-2022-SUNARP-SN. Gobierno del Perú.
Superintendencia Nacional de los Registros Públicos. (2026a). Resolución Jefatural N.° 055-2026-SUNARP/ZRXII/JEF. Gobierno del Perú.
Superintendencia Nacional de los Registros Públicos. (2026b). Resoluciones sobre cancelación administrativa por falsificación documental. Gobierno del Perú.
