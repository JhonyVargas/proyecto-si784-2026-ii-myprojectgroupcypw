<center>

![./media/media/image1.png](./media/logo-upt.png)

# **UNIVERSIDAD PRIVADA DE TACNA**

## **FACULTAD DE INGENIERIA**

### **Escuela Profesional de Ingeniería de Sistemas**

<br><br>

### **Proyecto**

## ***NotaryVerify – Sistema de Verificación de Identidad para Trámites Notariales***

<br>

Curso: *CALIDAD Y PRUEBAS DE SOFTWARE*

<br>

Docente: *PATRICK JOSE CUADROS QUIROGA*

<br><br>

Integrantes:

*Cohaila Alvarado, Gabriela Estefania (2022075746)*  
*Vargas Luque, Jhony (2022075754)*

<br><br><br><br>

**Tacna – Perú**  
***2026***

</center>

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

| CONTROL DE VERSIONES |           |              |              |            |                                               |
|----------------------|-----------|--------------|--------------|------------|-----------------------------------------------|
| Versión              | Hecha por | Revisada por | Aprobada por | Fecha      | Motivo                                        |
| 1.0                  | GC y JV   | PJCQ         | PJCQ         | 25/08/2026 | Versión Original                              |
| 1.1                  | GC y JV   | PJCQ         | PJCQ         | 26/08/26   | Información del sistema con temas y subtemas. |

<br><br><br><br><br>

<div align="right">

## **Sistema** ***NotaryVerify***
## **Documento de Visión**

### **Versión** ***{1.1}***

</div>

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

| CONTROL DE VERSIONES |           |              |              |            |                  |
|----------------------|-----------|--------------|--------------|------------|------------------|
| Versión              | Hecha por | Revisada por | Aprobada por | Fecha      | Motivo           |
| 1.0                  | MPV       | ELV          | ARV          | 10/10/2020 | Versión Original |

<br>

<center>

## **INDICE GENERAL**

</center>

[**1. Introducción 5**](#introducción)

[1.1 Propósito 5](#propósito)

[1.2 Alcance 6](#alcance)

[Fuera del alcance 8](#fuera-del-alcance)

[1.3 Definiciones, Siglas y Abreviaturas 8](#definiciones-siglas-y-abreviaturas)

[1.4 Referencias 11](#referencias)

[1.5 Visión General 11](#visión-general)

[**2. Posicionamiento 13**](#posicionamiento)

[2.1 Oportunidad de negocio 14](#oportunidad-de-negocio)

[2.2 Definición del problema 16](#definición-del-problema)

[**3. Descripción de los interesados y usuarios 17**](#descripción-de-los-interesados-y-usuarios)

[3.1 Resumen de los interesados 17](#resumen-de-los-interesados)

[3.2 Resumen de los usuarios 19](#resumen-de-los-usuarios)

[3.3 Entorno de usuario 20](#entorno-de-usuario)

[1. Estación de verificación 20](#estación-de-verificación)

[2. Entorno administrativo 20](#entorno-administrativo)

[3. Entorno de auditoría 21](#entorno-de-auditoría)

[4. Entorno biométrico 21](#entorno-biométrico)

[5. Entorno de integración simulada 21](#entorno-de-integración-simulada)

[3.4 Perfiles de los interesados 22](#perfiles-de-los-interesados)

[Personal relacionado con identificación notarial 22](#personal-relacionado-con-identificación-notarial)

[Responsable o supervisor 22](#responsable-o-supervisor)

[Responsable de auditoría 22](#responsable-de-auditoría)

[Participantes voluntarios 23](#participantes-voluntarios)

[Equipo de desarrollo 23](#equipo-de-desarrollo)

[3.5 Perfiles de los usuarios 23](#perfiles-de-los-usuarios)

[Operador de verificación 23](#operador-de-verificación)

[Administrador 24](#administrador)

[Auditor / Supervisor 25](#auditor-supervisor)

[Participante de prueba 25](#participante-de-prueba)

[3.6 Necesidades de los interesados y usuarios 25](#necesidades-de-los-interesados-y-usuarios)

[**4. Vista General del Producto 28**](#vista-general-del-producto)

[4.1 Perspectiva del producto 28](#perspectiva-del-producto)

[4.2 Resumen de capacidades 31](#resumen-de-capacidades)

[4.3 Suposiciones y dependencias 33](#suposiciones-y-dependencias)

[Suposiciones 33](#suposiciones)

[Dependencias internas 34](#dependencias-internas)

[Dependencias tecnológicas previstas 35](#dependencias-tecnológicas-previstas)

[Dependencias externas simuladas 35](#dependencias-externas-simuladas)

[Sistemas que NO constituyen dependencias obligatorias 35](#sistemas-que-no-constituyen-dependencias-obligatorias)

[4.4 Licenciamiento e instalación 36](#licenciamiento-e-instalación)

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# 1. Introducción

El presente Documento de Visión describe los objetivos, alcance, características generales, usuarios, necesidades, restricciones y principales capacidades del sistema **NotaryVerify – Sistema Experimental de Verificación de Identidad para Trámites Notariales**. El proyecto está orientado al estudio y desarrollo de un mecanismo experimental de verificación multicapa de identidad que permita evaluar, dentro de un entorno académico controlado, diferentes mecanismos tecnológicos destinados a detectar escenarios de intento de suplantación de identidad antes de continuar con un trámite notarial simulado.

NotaryVerify surge a partir de la necesidad de analizar cómo distintas técnicas de identificación y seguridad pueden actuar de manera complementaria, evitando que la validación de un único mecanismo sea considerada suficiente para determinar que una identidad ha sido verificada. Para ello, el prototipo propone combinar credenciales electrónicas QR/RFID, reconocimiento facial local, prueba de vida, reglas de seguridad, sesiones de verificación, controles de integridad documental mediante SHA-256 y una bitácora de auditoría con encadenamiento criptográfico.

El sistema será desarrollado exclusivamente con fines académicos y experimentales. No pretende sustituir los mecanismos oficiales utilizados por las notarías, Reniec, SID-Sunarp, certificados de firma digital u otros servicios institucionales. Las interacciones necesarias con este tipo de servicios serán representadas mediante componentes simulados desarrollados específicamente para el proyecto. Asimismo, las pruebas se realizarán utilizando identidades ficticias, documentos simulados y datos biométricos pertenecientes únicamente a participantes voluntarios que hayan autorizado expresamente su utilización.

Esta delimitación permitirá que NotaryVerify pueda ser utilizado para analizar escenarios controlados de verificación legítima, rechazo, utilización de credenciales inválidas o revocadas, falta de coincidencia facial, presentación de fotografías estáticas, fallos en pruebas de vida, modificaciones de documentos, intentos repetitivos de autenticación y errores producidos durante la comunicación con servicios externos simulados.

## 1.1 Propósito

El propósito del presente Documento de Visión es establecer una descripción general y compartida de **NotaryVerify**, definiendo el problema que se busca estudiar, los usuarios e interesados involucrados, las principales necesidades identificadas, las capacidades esperadas del producto, sus restricciones y los criterios generales que orientarán su posterior especificación, desarrollo y validación.

El propósito principal del sistema es desarrollar y evaluar un prototipo experimental de verificación multicapa de identidad aplicable a trámites notariales simulados. El sistema buscará comprobar que una identidad de prueba haya superado satisfactoriamente diversos mecanismos independientes antes de producir un resultado de verificación.

Para alcanzar este propósito, NotaryVerify integrará mecanismos de identificación electrónica mediante credenciales QR y RFID, reconocimiento facial ejecutado localmente, prueba de vida mediante desafíos faciales, reglas de decisión, control de intentos fallidos, sesiones de verificación, integridad documental mediante funciones hash SHA-256 y auditoría de operaciones críticas.

La finalidad de aplicar múltiples factores consiste en evitar que un único elemento determine el resultado final. Por ejemplo, la presentación de una credencial válida no permitirá aprobar una identidad cuando el rostro capturado no corresponda con la referencia registrada. De manera similar, una coincidencia facial no será considerada suficiente cuando la prueba de vida haya sido rechazada.

Asimismo, el proyecto tiene como propósito proporcionar un entorno académico en el que sea posible reproducir diferentes escenarios de suplantación y medir el comportamiento del sistema. Esto permitirá analizar resultados de aceptación, rechazo, falsos positivos, falsos negativos, fallos de integración y comportamiento frente a intentos repetitivos de verificación.

NotaryVerify no proporcionará una certificación oficial de identidad. Cuando el sistema indique **“IDENTIDAD VERIFICADA”**, dicho resultado significará únicamente que la persona evaluada superó los controles experimentales definidos dentro del prototipo. La identificación con efectos legales continuará dependiendo de las autoridades, procedimientos y sistemas oficialmente habilitados.

## 1.2 Alcance

El alcance del proyecto comprende el análisis, diseño, desarrollo y validación de una aplicación web experimental destinada a representar un proceso completo de verificación de identidad asociado a trámites notariales ficticios.

NotaryVerify permitirá crear y administrar identidades ficticias mediante un componente denominado **Simulador de Identidad**, el cual funcionará como una fuente de información académica equivalente únicamente para fines de prueba a una consulta institucional. Este simulador podrá almacenar identificadores ficticios, nombres simulados, fotografías de referencia autorizadas, estados de registro y otros atributos necesarios para ejecutar los escenarios definidos en el proyecto.

El sistema permitirá asociar las identidades simuladas con credenciales electrónicas de prueba representadas mediante códigos QR o tarjetas RFID. Estas credenciales tendrán como finalidad identificar el registro que debe ser evaluado y no constituirán por sí mismas evidencia suficiente para aprobar una verificación.

Posteriormente, el sistema permitirá capturar mediante cámara el rostro de la persona que participa en la verificación y compararlo con la referencia biométrica asociada a la identidad seleccionada. Para ello se utilizarán tecnologías de reconocimiento facial local y herramientas de código abierto, evitando depender obligatoriamente de servicios biométricos comerciales.

Como mecanismo adicional, NotaryVerify incorporará una **prueba de vida experimental**, en la que el participante deberá responder a desafíos faciales determinados por el sistema, como parpadear o realizar movimientos establecidos. El propósito será evaluar si la persona observada se encuentra presente frente a la cámara y dificultar intentos básicos de suplantación mediante fotografías estáticas o imágenes mostradas desde otro dispositivo.

El alcance también comprende la implementación de un **motor de reglas de seguridad**, encargado de combinar los resultados obtenidos por los distintos factores. El sistema podrá utilizar reglas como:

- Credencial válida + rostro coincidente + prueba de vida superada = verificación aprobada.

- Credencial válida + rostro no coincidente = verificación rechazada.

- Credencial válida + prueba de vida fallida = verificación rechazada.

- Credencial inexistente = verificación rechazada.

- Credencial revocada = verificación rechazada.

- Múltiples intentos fallidos consecutivos = generación de alerta.

- Modificación de información biométrica = requerimiento de autorización administrativa.

Cada proceso generará una **sesión de verificación** única en la que se registrarán los mecanismos utilizados, los resultados parciales, fecha, hora, usuario responsable y decisión final.

El sistema también permitirá asociar una sesión aprobada con un trámite notarial ficticio para demostrar que, antes de registrar una determinada operación de prueba, se ejecutó previamente un proceso de comprobación de identidad.

Como mecanismo complementario de seguridad documental, NotaryVerify calculará huellas criptográficas mediante **SHA-256** sobre documentos generados dentro de los escenarios académicos. Estas huellas permitirán verificar posteriormente si un archivo mantiene el mismo contenido registrado originalmente o si ha sido alterado.

Los documentos simulados podrán incorporar códigos QR destinados a consultar información básica sobre su registro, estado e integridad, sin almacenar directamente información biométrica o datos personales dentro del propio código.

También se encuentra dentro del alcance una **bitácora de auditoría con encadenamiento criptográfico**, destinada a registrar eventos críticos y permitir la detección de modificaciones posteriores realizadas intencionalmente sobre los registros protegidos.

Adicionalmente, se implementará un **Simulador SID-Sunarp** que representará de manera simplificada la interacción con un servicio institucional externo. Este componente únicamente recibirá trámites ficticios cuyas sesiones de verificación hayan sido previamente aprobadas y permitirá probar situaciones de disponibilidad, indisponibilidad temporal, rechazo, respuesta incorrecta y tiempo de espera agotado.

### Fuera del alcance

El proyecto no comprenderá:

- Acceso directo a bases de datos reales de Reniec.

- Acceso real al SID-Sunarp.

- Emisión de certificaciones oficiales de identidad.

- Sustitución de procedimientos legales notariales.

- Utilización de certificados digitales institucionales reales.

- Utilización de información personal perteneciente a clientes reales de una notaría.

- Utilización de fotografías biométricas obtenidas de Internet.

- Almacenamiento de información biométrica directamente dentro de códigos QR o tarjetas RFID.

- Desarrollo de un sistema biométrico certificado para utilización legal.

- Sustitución de los controles de identificación establecidos por las autoridades competentes.

Las integraciones institucionales necesarias serán representadas mediante simuladores propios, permitiendo evaluar el comportamiento de NotaryVerify sin depender de credenciales gubernamentales, información confidencial ni servicios comerciales de pago.

## 1.3 Definiciones, Siglas y Abreviaturas

<table>
<colgroup>
<col style="width: 28%" />
<col style="width: 71%" />
</colgroup>
<thead>
<tr class="header">
<th><blockquote>
<p><strong>Término / Sigla</strong></p>
</blockquote></th>
<th><blockquote>
<p><strong>Definición</strong></p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>NotaryVerify</strong></p>
</blockquote></th>
<th><blockquote>
<p>Sistema experimental propuesto para evaluar mecanismos multicapa de verificación de identidad en trámites notariales simulados.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Suplantación de identidad</strong></p>
</blockquote></th>
<th><blockquote>
<p>Utilización indebida de los datos, documentos, credenciales o características asociadas a otra persona con el propósito de presentarse como ella dentro de un proceso determinado.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>Verificación multicapa</strong></p>
</blockquote></th>
<th><blockquote>
<p>Proceso en el que la decisión de aprobación o rechazo depende de la combinación de diferentes mecanismos independientes de comprobación.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Reconocimiento facial</strong></p>
</blockquote></th>
<th><blockquote>
<p>Técnica biométrica destinada a comparar características del rostro capturado con una referencia previamente registrada.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>Biometría</strong></p>
</blockquote></th>
<th><blockquote>
<p>Utilización de características físicas o de comportamiento de una persona para apoyar procesos de identificación o verificación.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Prueba de vida / Liveness</strong></p>
</blockquote></th>
<th><blockquote>
<p>Mecanismo experimental destinado a determinar si el rostro capturado corresponde a una persona presente frente a la cámara y no únicamente a una representación estática.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>Enrolamiento biométrico</strong></p>
</blockquote></th>
<th><blockquote>
<p>Proceso mediante el cual se registran muestras biométricas autorizadas para asociarlas con una identidad ficticia dentro del sistema.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>QR (Quick Response)</strong></p>
</blockquote></th>
<th><blockquote>
<p>Código bidimensional utilizado dentro del prototipo como credencial o mecanismo de consulta mediante un identificador o token.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>RFID (Radio Frequency Identification)</strong></p>
</blockquote></th>
<th><blockquote>
<p>Tecnología de identificación mediante radiofrecuencia utilizada en el proyecto para representar una credencial electrónica de prueba.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Token</strong></p>
</blockquote></th>
<th><blockquote>
<p>Valor o identificador utilizado para relacionar una credencial con un registro interno sin almacenar directamente información sensible en ella.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>SHA-256</strong></p>
</blockquote></th>
<th><blockquote>
<p>Función criptográfica de resumen utilizada para generar una huella digital del contenido de un documento y comprobar posteriormente su integridad.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Hash / Huella criptográfica</strong></p>
</blockquote></th>
<th><blockquote>
<p>Resultado generado por una función criptográfica a partir de determinados datos. Una modificación del contenido produce una huella diferente.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>Integridad documental</strong></p>
</blockquote></th>
<th><blockquote>
<p>Propiedad que permite comprobar que un documento no ha sufrido modificaciones respecto de la versión previamente registrada.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Bitácora de auditoría</strong></p>
</blockquote></th>
<th><blockquote>
<p>Registro cronológico de eventos y operaciones realizadas dentro del sistema.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>Encadenamiento criptográfico</strong></p>
</blockquote></th>
<th><blockquote>
<p>Mecanismo mediante el cual un registro se relaciona criptográficamente con el anterior, facilitando la detección de alteraciones posteriores.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Sesión de verificación</strong></p>
</blockquote></th>
<th><blockquote>
<p>Registro único que agrupa la identidad evaluada, factores utilizados, resultados parciales, usuario responsable, fecha, hora y decisión final.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>Simulador de Identidad</strong></p>
</blockquote></th>
<th><blockquote>
<p>Servicio desarrollado para el proyecto que almacena y consulta exclusivamente identidades ficticias y representa académicamente una fuente institucional de identidad.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Simulador SID-Sunarp</strong></p>
</blockquote></th>
<th><blockquote>
<p>Servicio experimental que representa de manera simplificada la interacción de NotaryVerify con un sistema institucional externo para fines de prueba.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>SID-Sunarp</strong></p>
</blockquote></th>
<th><blockquote>
<p>Sistema de Intermediación Digital de la Superintendencia Nacional de los Registros Públicos.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Sunarp</strong></p>
</blockquote></th>
<th><blockquote>
<p>Superintendencia Nacional de los Registros Públicos.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>Reniec</strong></p>
</blockquote></th>
<th><blockquote>
<p>Registro Nacional de Identificación y Estado Civil.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>API</strong></p>
</blockquote></th>
<th><blockquote>
<p>Interfaz que permite la comunicación estructurada entre diferentes componentes o servicios de software.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>Falso positivo</strong></p>
</blockquote></th>
<th><blockquote>
<p>Resultado en el que el sistema acepta incorrectamente un caso que debía ser rechazado.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Falso negativo</strong></p>
</blockquote></th>
<th><blockquote>
<p>Resultado en el que el sistema rechaza incorrectamente un caso legítimo que debía ser aceptado.</p>
</blockquote></th>
</tr>
<tr class="odd">
<th><blockquote>
<p><strong>Dato biométrico</strong></p>
</blockquote></th>
<th><blockquote>
<p>Información obtenida a partir de características físicas o conductuales utilizada para identificar o verificar a una persona.</p>
</blockquote></th>
</tr>
<tr class="header">
<th><blockquote>
<p><strong>Trámite ficticio</strong></p>
</blockquote></th>
<th><blockquote>
<p>Representación académica de una operación notarial utilizada únicamente para ejecutar y evaluar pruebas dentro del proyecto.</p>
</blockquote></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Los conceptos anteriores delimitan la terminología que será utilizada de manera consistente a lo largo de los documentos posteriores de NotaryVerify.

## 1.4 Referencias

Para la elaboración inicial del proyecto y la definición de las tecnologías, restricciones legales y mecanismos experimentales se consideran las siguientes referencias proporcionadas en la propuesta del sistema:

- Ministerio de Justicia y Derechos Humanos. (2024). *Decreto Supremo N.° 016-2024-JUS: Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales*. Gobierno del Perú.

- OpenCV. (2026). *FaceRecognizerSF*. OpenCV Java Documentation.

- OpenCV. (2026). *OpenCV Zoo: SFace Face Recognition Model*.

- Google. (2026). *MediaPipe Face Landmarker*. Google AI for Developers.

- Superintendencia Nacional de los Registros Públicos. (2023). *Resolución de la Superintendencia Nacional de los Registros Públicos N.° 169-2023-SUNARP/SN*. Gobierno del Perú.

- Superintendencia Nacional de los Registros Públicos. (2026a). *Resolución Jefatural N.° 055-2026-SUNARP/ZRXII/JEF*. Gobierno del Perú.

- Superintendencia Nacional de los Registros Públicos. (2026b). *Resoluciones relacionadas con cancelación de asientos registrales por falsificación documental*. Gobierno del Perú.

Estas referencias sustentan inicialmente tres aspectos principales del proyecto: el contexto notarial y registral relacionado con la necesidad de proteger la identidad y autenticidad documental; las restricciones relacionadas con el tratamiento de datos personales y biométricos; y la viabilidad técnica de implementar mecanismos experimentales de reconocimiento facial y análisis de características faciales utilizando herramientas de desarrollo disponibles.

## 1.5 Visión General

NotaryVerify se concibe como una aplicación web experimental organizada alrededor de un proceso de **verificación multicapa de identidad**, en el que diferentes componentes participan progresivamente hasta producir una decisión final.

De manera general, el flujo del sistema será:

```text
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

↓

REGISTRO Y AUDITORÍA

```

El proceso comenzará cuando una credencial QR o RFID permita identificar qué registro ficticio deberá ser evaluado. El sistema consultará posteriormente el **Simulador de Identidad**, obteniendo la información necesaria y la referencia biométrica asociada.

A continuación, se realizará la captura facial y la comparación con las muestras previamente enroladas. Posteriormente, la prueba de vida solicitará al participante realizar una acción determinada para evaluar que se encuentre presente frente a la cámara.

Los resultados obtenidos serán enviados al motor de reglas, encargado de determinar si la sesión debe ser aprobada, rechazada, marcada como sospechosa o enviada a revisión.

Entre los posibles resultados se contemplan:

- **IDENTIDAD VERIFICADA**

- **VERIFICACIÓN RECHAZADA**

- **ROSTRO NO COINCIDENTE**

- **PRUEBA DE VIDA FALLIDA**

- **CREDENCIAL NO REGISTRADA**

- **CREDENCIAL REVOCADA**

- **MÚLTIPLES INTENTOS FALLIDOS**

- **VERIFICACIÓN REQUIERE REVISIÓN**

Cada decisión será almacenada dentro de una sesión de verificación junto con sus evidencias y metadatos asociados.

Cuando una sesión haya sido aprobada, podrá vincularse con un trámite notarial ficticio. Los documentos generados durante este proceso podrán ser protegidos mediante una huella SHA-256 y consultados posteriormente a través de mecanismos de verificación QR.

Paralelamente, las operaciones críticas serán registradas dentro de una bitácora de auditoría con mecanismos destinados a detectar alteraciones posteriores.

Finalmente, determinados trámites ficticios podrán ser enviados al **Simulador SID-Sunarp**, permitiendo reproducir el comportamiento de una integración externa y evaluar respuestas exitosas, rechazos, errores o indisponibilidad.

De esta forma, NotaryVerify no se limita a responder si un rostro coincide con una fotografía. Su enfoque consiste en **combinar múltiples evidencias, reglas y controles para construir una decisión verificable y auditable**, conservando la trazabilidad de los mecanismos utilizados durante cada proceso.

El sistema será desarrollado bajo una arquitectura orientada a mantener separados los principales dominios funcionales: gestión de identidades ficticias, credenciales, biometría, prueba de vida, verificación, documentos, auditoría y servicios institucionales simulados. Esta separación permitirá posteriormente probar cada componente de manera independiente y también validar el comportamiento integral del sistema frente a los escenarios definidos en el proyecto.

# 2. Posicionamiento

NotaryVerify se posiciona como una **solución experimental complementaria de verificación de identidad**, orientada a estudiar cómo la combinación de distintos controles tecnológicos puede contribuir a detectar intentos de suplantación antes de continuar con un trámite notarial simulado. Su propuesta de valor no consiste en reemplazar los mecanismos oficiales de identificación utilizados por las notarías ni los servicios de entidades como Reniec o Sunarp, sino en implementar una capa previa de verificación que permita reunir, contrastar y registrar diferentes evidencias de identidad dentro de un mismo proceso.

A diferencia de un sistema basado únicamente en la presentación de un documento, una credencial o una comparación facial aislada, NotaryVerify plantea que la decisión final dependa de la evaluación conjunta de varios factores: credencial QR o RFID, registro de identidad ficticia, reconocimiento facial, prueba de vida, reglas de seguridad, historial de intentos y controles de auditoría. Esta combinación permite representar escenarios en los que un factor aparentemente válido no sea suficiente para aprobar la operación cuando otro mecanismo produzca un resultado incompatible.

El sistema se orienta principalmente a un contexto académico y de experimentación, en el que sea posible reproducir tanto verificaciones legítimas como diferentes intentos controlados de suplantación. De esta manera, el proyecto permitirá obtener evidencia sobre el comportamiento de los mecanismos implementados, sus limitaciones y la utilidad de emplearlos de forma complementaria.

## 2.1 Oportunidad de negocio

La correcta identificación de las personas constituye un elemento relevante dentro de los procedimientos notariales y registrales, debido a que una actuación realizada utilizando la identidad de otra persona puede generar consecuencias jurídicas, administrativas y registrales posteriores. La propuesta del proyecto parte precisamente de la existencia de este riesgo y de la necesidad de evaluar mecanismos tecnológicos adicionales que permitan reforzar la verificación previa de identidad.

La problemática posee relevancia dentro del contexto peruano. En la propuesta del proyecto se identifican actuaciones registrales recientes vinculadas con presunta suplantación de identidad y falsificación documental. Asimismo, se reconoce que el sistema registral peruano ya dispone de mecanismos oficiales de seguridad, como el **SID-Sunarp** y la utilización de firma digital para determinados actos inscribibles. Por ello, la oportunidad que aborda NotaryVerify no se encuentra en sustituir dichos sistemas, sino en investigar una **capa tecnológica previa y complementaria** que pueda evaluar diferentes factores antes de autorizar la continuación de una operación simulada.

Desde una perspectiva tecnológica, existe una oportunidad de integrar en un único flujo controles que normalmente pueden analizarse de manera independiente. El reconocimiento facial permite comprobar la similitud entre el rostro presentado y una referencia previamente registrada; la prueba de vida busca disminuir la posibilidad de utilizar fotografías estáticas; las credenciales QR o RFID permiten recuperar de manera controlada el registro que debe verificarse; y el motor de reglas permite decidir cómo deben interpretarse conjuntamente los resultados obtenidos.

La oportunidad principal del sistema se encuentra, por tanto, en **evitar que una sola comprobación determine por sí misma que la identidad ha sido validada**. Por ejemplo, disponer físicamente de una credencial válida no debería ser suficiente cuando el rostro presentado no coincide con la identidad asociada. De igual forma, una coincidencia facial no debería aprobar automáticamente la verificación cuando la prueba de vida determine que el desafío solicitado no fue superado.

NotaryVerify también presenta una oportunidad en materia de **trazabilidad y auditoría**. Cada proceso de verificación podrá generar una sesión única en la que se almacenen los factores utilizados, sus resultados individuales, la fecha y hora, el usuario responsable y la decisión final. Esto permitirá reconstruir posteriormente cómo se produjo una determinada aprobación o rechazo, en lugar de conservar únicamente un resultado final sin evidencia sobre el procedimiento seguido.

A esta trazabilidad se incorporarán mecanismos complementarios de protección de documentos. El uso de SHA-256 permitirá registrar una huella criptográfica de los archivos de prueba y detectar modificaciones posteriores, mientras que la bitácora con encadenamiento criptográfico permitirá experimentar con mecanismos destinados a evidenciar alteraciones realizadas sobre eventos protegidos.

Otra oportunidad relevante corresponde a la posibilidad de **evaluar escenarios adversos sin depender de sistemas institucionales reales**. El proyecto implementará servicios simulados, principalmente un Simulador de Identidad y un Simulador SID-Sunarp. Estos componentes permitirán reproducir respuestas exitosas, registros inexistentes, errores, indisponibilidad y tiempos de espera agotados, haciendo posible evaluar el comportamiento del sistema ante fallos externos sin utilizar credenciales institucionales ni información confidencial.

Esta estrategia también reduce las barreras de implementación académica. Debido a que el prototipo utilizará tecnologías locales y de código abierto para los componentes biométricos y desarrollará sus propias simulaciones de servicios externos, será posible construir y probar la solución sin depender obligatoriamente de API comerciales de pago, bases de datos gubernamentales o certificados institucionales reales.

Desde el punto de vista de calidad y pruebas de software, NotaryVerify ofrece además una oportunidad especialmente adecuada para el curso, debido a que presenta múltiples escenarios verificables: credencial válida, inexistente o revocada; rostro correcto o incorrecto; prueba de vida satisfactoria o fallida; documento original o alterado; servicio externo disponible o indisponible; intentos únicos o repetitivos; y operaciones permitidas o restringidas según el rol.

Esto permitirá que el sistema no sea evaluado únicamente por la existencia de sus funcionalidades, sino mediante métricas y pruebas sobre el comportamiento de los mecanismos implementados. La propuesta ya establece, entre otros objetivos, la realización de al menos **100 intentos biométricos controlados**, la medición de aceptaciones, rechazos, falsos positivos y falsos negativos, la evaluación de la prueba de vida frente a personas reales y fotografías, una cobertura objetivo igual o superior al **80 %** en componentes seleccionados y trazabilidad del **100 % de los requerimientos de prioridad alta**.

Por estas razones, la oportunidad que representa NotaryVerify puede resumirse como el desarrollo de un entorno experimental que permita **integrar, probar y medir mecanismos complementarios de verificación de identidad**, generando evidencia sobre su funcionamiento conjunto y proporcionando una base tecnológica que, bajo las correspondientes evaluaciones legales, técnicas y de seguridad, podría servir posteriormente como referencia para soluciones de apoyo en procesos donde la comprobación de identidad tenga especial relevancia.

## 2.2 Definición del problema

Siguiendo la estructura utilizada en el Documento de Visión tomado como referencia, la problemática central puede sintetizarse de la siguiente manera:

| **Elemento**                   | **Descripción**                                                                                                                                                                                                                                                                                                                                                             |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **El problema de**             | El riesgo de que una persona intente intervenir en un trámite notarial utilizando una identidad, credencial, documento o referencia perteneciente a otra persona, unido a la necesidad de estudiar mecanismos complementarios que permitan detectar estos escenarios antes de continuar con la operación.                                                                   |
| **Afecta a**                   | Personal encargado de realizar procesos de identificación y atención dentro del escenario notarial estudiado, responsables de supervisión y auditoría, así como a las personas cuya identidad podría ser utilizada indebidamente. Dentro del prototipo académico, también afecta a los usuarios responsables de ejecutar y revisar las verificaciones simuladas.            |
| **Cuyo impacto es**            | La posibilidad de que una operación continúe utilizando una identidad incorrecta o evidencia insuficiente de verificación, generando riesgos posteriores sobre la autenticidad del trámite, necesidad de revisión, dificultades para reconstruir cómo se realizó la comprobación y potenciales consecuencias jurídicas, administrativas o registrales en un escenario real. |
| **Una solución exitosa sería** | Un sistema experimental que combine credenciales QR/RFID, reconocimiento facial, prueba de vida, reglas multicapa, control de intentos, integridad documental y auditoría, de manera que ninguna validación aislada sea suficiente para aprobar una identidad y que cada decisión quede respaldada por una sesión de verificación trazable y auditable.                     |

La problemática puede expresarse con mayor precisión señalando que **NotaryVerify no busca resolver la identificación legal de una persona**, ya que esa responsabilidad corresponde a los procedimientos y sistemas oficialmente habilitados. El problema abordado por el proyecto consiste específicamente en determinar si una combinación de mecanismos tecnológicos complementarios puede mejorar la capacidad de detectar escenarios controlados de suplantación frente a la utilización aislada de un solo mecanismo.

En este sentido, el proyecto estudiará casos como la presentación de una credencial perteneciente a otra identidad, utilización de una credencial revocada, presentación de un rostro diferente al registrado, intento de superar el reconocimiento mediante una fotografía, repetición consecutiva de verificaciones fallidas y modificación posterior de documentos relacionados con una sesión aprobada.

El sistema deberá responder a estos escenarios siguiendo reglas previamente definidas y conservar evidencia suficiente para determinar posteriormente **qué ocurrió, qué controles fueron aplicados, qué resultado produjo cada uno y por qué se tomó la decisión final**.

La solución propuesta se diferencia así de una verificación binaria basada únicamente en “válido/no válido”. NotaryVerify pretende construir una decisión basada en múltiples evidencias independientes y proporcionar trazabilidad sobre todo el proceso, manteniendo siempre su condición de **prototipo académico experimental sin valor de identificación legal**.

# 3. Descripción de los interesados y usuarios

La identificación de interesados y usuarios permite establecer quiénes se encuentran relacionados con el desarrollo, validación, utilización y supervisión de **NotaryVerify – Sistema Experimental de Verificación de Identidad para Trámites Notariales**.

Debido al carácter académico del proyecto, se diferencia entre los actores que podrían estar involucrados en un contexto notarial real y aquellos que participarán directamente durante las pruebas controladas del prototipo. Esta distinción es importante porque NotaryVerify no será utilizado para realizar verificaciones legales de identidad ni procesará información real de clientes de una notaría. Todas las operaciones serán ejecutadas con identidades ficticias, trámites simulados y datos biométricos pertenecientes únicamente a participantes voluntarios autorizados.

Los principales interesados incluyen al personal relacionado con procesos de identificación y supervisión notarial, responsables de auditoría, equipo de desarrollo, participantes voluntarios y responsables académicos. Por otra parte, los usuarios directos del sistema serán aquellos que interactúen con las funcionalidades de registro, enrolamiento, verificación, administración y auditoría.

## 3.1 Resumen de los interesados

Los interesados representan a las personas o grupos que tienen algún interés en el desarrollo, funcionamiento, evaluación o resultados de NotaryVerify, aunque no necesariamente interactúen directamente con todas las funcionalidades del sistema.

| **Interesado**                                              | **Descripción**                                                                                                                                  | **Interés principal**                                                                                                                         |
|-------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| **Personal de atención o identificación notarial**          | Representa al personal que, dentro del proceso estudiado, participa en la recepción de personas, documentos y comprobación inicial de identidad. | Contar con mecanismos complementarios que permitan detectar inconsistencias antes de continuar con un trámite.                                |
| **Responsable o supervisor notarial**                       | Persona encargada de supervisar que los procedimientos se desarrollen correctamente y revisar situaciones que requieran evaluación adicional.    | Disponer de información trazable sobre las verificaciones realizadas y poder revisar resultados sospechosos o rechazados.                     |
| **Responsable de auditoría o control**                      | Interesado en revisar posteriormente los eventos registrados, decisiones tomadas y operaciones ejecutadas dentro del sistema.                    | Tener evidencia íntegra y cronológica de las operaciones críticas realizadas durante cada proceso de verificación.                            |
| **Equipo de desarrollo del proyecto**                       | Integrantes responsables del análisis, diseño, implementación, pruebas y documentación de NotaryVerify.                                          | Construir y validar un prototipo funcional que cumpla los objetivos de investigación y solución definidos.                                    |
| **Participantes voluntarios de las pruebas biométricas**    | Personas que autorizan expresamente el uso de sus muestras faciales únicamente para los experimentos académicos del proyecto.                    | Que sus datos biométricos sean utilizados de manera limitada, controlada y exclusivamente para las pruebas autorizadas.                       |
| **Docente del curso**                                       | Responsable académico de revisar el avance, calidad, cumplimiento documental y resultados del proyecto.                                          | Verificar que el proyecto cumpla los objetivos del curso de Calidad y Pruebas de Software y que exista evidencia suficiente de su validación. |
| **Escuela Profesional de Ingeniería de Sistemas de la UPT** | Entorno académico en el que se desarrolla y evalúa el proyecto.                                                                                  | Que el proyecto demuestre aplicación práctica de análisis, calidad, pruebas, seguridad, trazabilidad y documentación de software.             |

En un eventual escenario de investigación futura, también podrían considerarse como interesados organismos como Reniec o Sunarp debido a su relación con procesos oficiales de identidad y registro. Sin embargo, **no serán participantes operativos ni proveedores reales de información dentro del presente proyecto**, ya que NotaryVerify utilizará servicios institucionales simulados.

## 3.2 Resumen de los usuarios

Los usuarios corresponden a los actores que interactuarán directamente con NotaryVerify durante la ejecución del prototipo.

| **Nombre del usuario**        | **Descripción**                                                                                                                                                                | **Rol en el sistema**                          |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| **Operador de verificación**  | Usuario encargado de iniciar procesos de verificación, leer credenciales QR/RFID, solicitar la captura facial, ejecutar la prueba de vida y consultar el resultado obtenido.   | Ejecuta verificaciones de identidad simuladas. |
| **Administrador del sistema** | Usuario con permisos elevados para configurar el sistema, administrar cuentas, gestionar identidades ficticias, enrolamientos, credenciales, reglas y parámetros de seguridad. | Administración y configuración.                |
| **Auditor / Supervisor**      | Usuario encargado de consultar sesiones históricas, alertas, eventos, resultados de verificaciones y registros de auditoría.                                                   | Supervisión y auditoría.                       |
| **Participante de prueba**    | Persona voluntaria que se presenta ante la cámara y utiliza una identidad ficticia previamente asociada para participar en escenarios biométricos controlados.                 | Sujeto evaluado durante las pruebas.           |
| **Servicio externo simulado** | Componente automatizado, como el Simulador de Identidad o Simulador SID-Sunarp, que intercambia información con NotaryVerify durante determinados flujos.                      | Integración automatizada.                      |

Aunque el participante voluntario interviene directamente en el proceso, no necesariamente tendrá una cuenta de acceso al sistema. Su interacción se produce principalmente mediante la presentación de la credencial, la captura facial y la ejecución de los desafíos de prueba de vida.

Los servicios simulados tampoco son usuarios humanos, pero se incluyen dentro de la visión del producto porque representan actores externos con los que NotaryVerify deberá comunicarse y cuyo comportamiento será evaluado durante las pruebas de integración.

## 3.3 Entorno de usuario

NotaryVerify será utilizado dentro de un **entorno académico controlado**, diseñado para reproducir de manera simplificada determinadas etapas relacionadas con la verificación previa de identidad en un trámite notarial.

El sistema tendrá principalmente un entorno de interacción web y utilizará dispositivos complementarios para determinados mecanismos de verificación.

### 1. Estación de verificación

El operador utilizará una computadora o laptop con acceso a NotaryVerify desde un navegador web.

Desde esta estación podrá:

- iniciar una nueva sesión de verificación;

- leer una credencial QR o RFID;

- consultar la identidad ficticia asociada;

- activar la captura mediante cámara;

- ejecutar el reconocimiento facial;

- iniciar la prueba de vida;

- visualizar el resultado de los factores evaluados;

- consultar la decisión final del motor de reglas;

- asociar una sesión aprobada con un trámite ficticio.

La estación deberá disponer de una cámara compatible para realizar las pruebas biométricas.

### 2. Entorno administrativo

El administrador accederá mediante una interfaz web autenticada desde la que podrá realizar operaciones restringidas como:

- registrar identidades ficticias;

- modificar el estado de una identidad;

- gestionar usuarios y roles;

- realizar enrolamientos biométricos;

- emitir o revocar credenciales de prueba;

- configurar reglas de seguridad;

- consultar alertas;

- administrar determinados parámetros del sistema.

Las operaciones críticas deberán estar restringidas mediante controles de acceso basados en roles, de acuerdo con los objetivos definidos para el proyecto.

### 3. Entorno de auditoría

Los usuarios autorizados podrán consultar información histórica relacionada con las verificaciones realizadas.

Entre la información disponible podrán encontrarse:

- identificador de sesión;

- identidad ficticia evaluada;

- fecha y hora;

- usuario responsable;

- credencial utilizada;

- resultado del reconocimiento facial;

- resultado de la prueba de vida;

- reglas aplicadas;

- decisión final;

- alertas generadas;

- eventos relacionados.

La bitácora permitirá reconstruir posteriormente el desarrollo de una verificación y comprobar la integridad de determinados eventos protegidos mediante encadenamiento criptográfico.

### 4. Entorno biométrico

Las pruebas de reconocimiento facial y liveness se realizarán mediante una cámara conectada al equipo de prueba.

Los participantes deberán haber autorizado previamente el uso de sus datos biométricos y las muestras obtenidas se vincularán únicamente con identidades ficticias creadas específicamente para el proyecto.

No se utilizarán imágenes de ciudadanos obtenidas desde Internet ni datos pertenecientes a clientes reales de una notaría.

### 5. Entorno de integración simulada

NotaryVerify se comunicará con servicios desarrollados específicamente para representar dependencias institucionales.

Entre ellos se contemplan:

**Simulador de Identidad:** permitirá consultar registros ficticios y reproducir situaciones como identidad existente, identidad inexistente, fotografía diferente, servicio disponible o indisponible.

**Simulador SID-Sunarp:** permitirá representar el envío de un trámite ficticio después de una verificación aprobada y reproducir respuestas de aceptación, rechazo, error o indisponibilidad.

Estas integraciones permitirán ejecutar pruebas de comportamiento sin acceder a sistemas reales de Reniec o Sunarp.

## 3.4 Perfiles de los interesados

### Personal relacionado con identificación notarial

Corresponde al personal cuyo proceso de trabajo sirve como referencia para el escenario que busca representar NotaryVerify.

Su principal interés se encuentra en contar con información suficiente para decidir si una operación puede continuar o si requiere una revisión adicional.

No se espera que este perfil posea conocimientos avanzados de biometría, criptografía o desarrollo de software. Por ello, el sistema deberá presentar los resultados de manera comprensible, evitando que el usuario tenga que interpretar directamente métricas técnicas complejas.

Por ejemplo, en lugar de mostrar únicamente valores internos del algoritmo, la interfaz debería presentar resultados como:

**Rostro coincidente**,  
**Rostro no coincidente**,  
**Prueba de vida superada**,  
**Prueba de vida fallida**,  
**Verificación aprobada**,  
**Verificación rechazada**.

### Responsable o supervisor

Este perfil requiere una visión más completa sobre los procesos ejecutados.

Debe poder identificar:

- verificaciones aprobadas;

- verificaciones rechazadas;

- sesiones enviadas a revisión;

- intentos repetidos;

- credenciales revocadas;

- inconsistencias encontradas;

- operaciones realizadas por cada usuario.

Su interés principal se encuentra en disponer de trazabilidad suficiente para analizar situaciones excepcionales.

### Responsable de auditoría

El auditor tiene como objetivo revisar el historial del sistema y verificar que las operaciones realizadas puedan reconstruirse posteriormente.

Necesita conocer:

- quién ejecutó una operación;

- cuándo se realizó;

- sobre qué identidad ficticia;

- qué mecanismos fueron utilizados;

- qué resultado produjo cada factor;

- cuál fue la decisión final;

- si existieron modificaciones posteriores sobre registros protegidos.

Por ello, este perfil tiene especial interés en las sesiones de verificación, bitácora de eventos, integridad documental y encadenamiento criptográfico.

### Participantes voluntarios

Son las personas cuyas muestras biométricas serán utilizadas durante los experimentos.

Su principal necesidad no corresponde a la utilización funcional del sistema, sino a la protección de la información proporcionada.

El proyecto establece que las muestras únicamente podrán corresponder a voluntarios autorizados y deberán utilizarse exclusivamente para los fines académicos definidos.

### Equipo de desarrollo

El equipo requiere acceso a los componentes técnicos del sistema para poder desarrollar, mantener, probar y evaluar el prototipo.

También será responsable de:

- preparar escenarios de prueba;

- mantener los servicios simulados;

- ejecutar pruebas automatizadas;

- revisar defectos;

- medir cobertura;

- registrar resultados;

- mantener la documentación y trazabilidad.

## 3.5 Perfiles de los usuarios

### Operador de verificación

**Nivel técnico:** básico o intermedio.

**Responsabilidad principal:** ejecutar correctamente el procedimiento de verificación.

El operador deberá poder utilizar el sistema sin comprender internamente los algoritmos de reconocimiento facial o las operaciones criptográficas realizadas.

Su flujo habitual será:

```text
Iniciar sesión

↓

Crear verificación

↓

Leer QR / RFID

↓

Consultar identidad ficticia

↓

Capturar rostro

↓

Ejecutar prueba de vida

↓

Esperar evaluación

↓

Consultar resultado

```

El sistema deberá proporcionar mensajes claros cuando una verificación no pueda continuar.

### Administrador

**Nivel técnico:** intermedio o avanzado.

**Responsabilidades principales:**

- gestionar usuarios;

- gestionar roles;

- administrar identidades ficticias;

- realizar enrolamientos;

- administrar credenciales;

- revocar credenciales;

- modificar determinados parámetros;

- gestionar reglas de seguridad;

- revisar alertas y configuraciones.

Debido al impacto de estas operaciones, deberán restringirse únicamente a usuarios debidamente autorizados. La propuesta establece como objetivo que el **100 % de las operaciones críticas de configuración, enrolamiento, modificación y auditoría estén protegidas mediante controles basados en roles**.

### Auditor / Supervisor

**Nivel técnico:** intermedio.

Este usuario no requiere modificar la configuración principal del sistema.

Sus actividades estarán orientadas a:

- consultar sesiones;

- revisar verificaciones rechazadas;

- analizar alertas;

- comprobar eventos de auditoría;

- verificar integridad;

- revisar intentos consecutivos;

- consultar operaciones realizadas por otros usuarios.

La interfaz debe priorizar la consulta y trazabilidad de información.

### Participante de prueba

**Nivel técnico:** no requerido.

Su participación consistirá en seguir las instrucciones que el sistema presente durante los experimentos.

Por ejemplo:

```text
Mire hacia la cámara.

Parpadee.

Gire ligeramente el rostro hacia la derecha.

Mantenga el rostro visible.

```

No tendrá acceso a funciones administrativas ni de auditoría.

## 3.6 Necesidades de los interesados y usuarios

A partir del planteamiento del proyecto y de los objetivos definidos para NotaryVerify, pueden establecerse inicialmente las siguientes necesidades. Estas necesidades servirán posteriormente como base para definir y mantener trazabilidad con los requerimientos funcionales del FD03.

| **Código** | **Necesidad**                                                                                             | **Requerimiento funcional relacionado**                                                                   | **Prioridad** | **Importancia** |
|------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|---------------|-----------------|
| **N-01**   | Registrar identidades ficticias para realizar verificaciones sin utilizar información real de ciudadanos. | **RF01:** Gestionar identidades ficticias mediante el Simulador de Identidad.                             | Alta          | Crítica         |
| **N-02**   | Asociar referencias biométricas autorizadas con las identidades ficticias utilizadas durante las pruebas. | **RF02:** Realizar enrolamiento biométrico de participantes autorizados.                                  | Alta          | Crítica         |
| **N-03**   | Identificar de manera rápida qué registro debe ser verificado.                                            | **RF03:** Leer y validar credenciales QR/RFID vinculadas a identidades ficticias.                         | Alta          | Alta            |
| **N-04**   | Comprobar que el rostro presentado corresponde con la referencia registrada.                              | **RF04:** Ejecutar reconocimiento facial y generar un resultado de coincidencia.                          | Alta          | Crítica         |
| **N-05**   | Detectar intentos básicos de engaño mediante fotografías estáticas o pantallas.                           | **RF05:** Ejecutar una prueba de vida mediante desafíos faciales aleatorios.                              | Alta          | Crítica         |
| **N-06**   | Evitar que una única validación sea suficiente para aprobar una identidad.                                | **RF06:** Aplicar reglas multicapa sobre los factores obtenidos durante la verificación.                  | Alta          | Crítica         |
| **N-07**   | Registrar completamente cada proceso de comprobación de identidad.                                        | **RF07:** Crear y almacenar sesiones de verificación con resultados y metadatos.                          | Alta          | Crítica         |
| **N-08**   | Detectar múltiples verificaciones fallidas asociadas con un mismo contexto.                               | **RF08:** Registrar intentos fallidos y generar alertas al superar el límite configurado.                 | Alta          | Alta            |
| **N-09**   | Detectar modificaciones realizadas sobre documentos vinculados con operaciones verificadas.               | **RF09:** Calcular y validar huellas SHA-256 de documentos de prueba.                                     | Alta          | Alta            |
| **N-10**   | Permitir verificar posteriormente el estado de un documento de prueba.                                    | **RF10:** Generar códigos QR de consulta asociados con documentos registrados.                            | Media         | Alta            |
| **N-11**   | Mantener evidencia sobre las operaciones críticas realizadas dentro del sistema.                          | **RF11:** Registrar eventos en una bitácora de auditoría protegida mediante encadenamiento criptográfico. | Alta          | Crítica         |
| **N-12**   | Representar la interacción con servicios institucionales sin depender de sistemas gubernamentales reales. | **RF12:** Integrar el Simulador de Identidad y Simulador SID-Sunarp.                                      | Alta          | Alta            |
| **N-13**   | Evaluar el comportamiento del sistema cuando un servicio externo presenta fallos.                         | **RF13:** Simular respuestas exitosas, errores, rechazo, indisponibilidad y timeout.                      | Media         | Alta            |
| **N-14**   | Restringir las operaciones sensibles únicamente a personal autorizado.                                    | **RF14:** Implementar autenticación y control de acceso basado en roles.                                  | Alta          | Crítica         |
| **N-15**   | Consultar el historial completo de una verificación y conocer cómo se tomó la decisión final.             | **RF15:** Consultar sesiones, factores evaluados, resultados, usuario responsable y eventos asociados.    | Alta          | Crítica         |
| **N-16**   | Asociar una identidad verificada con una operación notarial ficticia.                                     | **RF16:** Vincular sesiones aprobadas con trámites notariales simulados.                                  | Media         | Alta            |
| **N-17**   | Impedir que un trámite ficticio avance cuando la identidad no haya superado los controles definidos.      | **RF17:** Autorizar el envío al Simulador SID-Sunarp únicamente cuando la sesión tenga estado aprobado.   | Alta          | Crítica         |

# 4. Vista General del Producto

NotaryVerify se concibe como una **aplicación web experimental de verificación multicapa de identidad**, diseñada para representar y evaluar, dentro de un entorno académico controlado, diferentes mecanismos tecnológicos destinados a detectar intentos de suplantación antes de continuar con un trámite notarial ficticio.

El producto integra en un mismo flujo diversos factores de verificación: credenciales QR/RFID, consulta de una identidad simulada, reconocimiento facial local, prueba de vida, reglas de seguridad, control de intentos fallidos, sesiones de verificación, integridad documental mediante SHA-256, códigos QR de consulta y una bitácora de auditoría con encadenamiento criptográfico.

El sistema no será considerado un mecanismo oficial de identificación ni sustituirá a Reniec, SID-Sunarp, firma digital, certificados oficiales ni procedimientos notariales establecidos. Sus resultados tendrán exclusivamente valor experimental dentro del proyecto.

## 4.1 Perspectiva del producto

NotaryVerify funcionará como una **capa experimental de verificación previa**, situada conceptualmente antes de que un trámite notarial ficticio continúe hacia una etapa posterior del proceso.

Su propósito no será administrar íntegramente una notaría ni reemplazar los sistemas institucionales existentes, sino concentrarse específicamente en el proceso de comprobación de identidad y en la conservación de evidencia sobre cómo dicha verificación fue realizada.

De manera general, el sistema seguirá el siguiente flujo:

```text
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

DECISIÓN FINAL

↓

REGISTRO Y AUDITORÍA

↓

TRÁMITE FICTICIO

```

El proceso comenzará con la identificación del registro que debe verificarse. Para ello, el participante presentará una credencial QR o RFID asociada con una identidad ficticia previamente registrada dentro del **Simulador de Identidad**.

La credencial no aprobará por sí misma la identidad. Su finalidad será únicamente recuperar el registro esperado para la verificación.

Posteriormente, el sistema utilizará la cámara para capturar el rostro de la persona participante y compararlo con la referencia biométrica asociada con la identidad ficticia.

Después de la comparación facial, se ejecutará una prueba de vida experimental mediante desafíos faciales. El objetivo será evaluar si la persona se encuentra presente frente a la cámara y detectar escenarios básicos en los que se intente utilizar una fotografía impresa o mostrada desde otra pantalla.

Los resultados individuales serán procesados por un **motor de reglas multicapa**, responsable de combinar los distintos factores y emitir una decisión.

Por ejemplo:

```text
Credencial válida

\+ Rostro coincidente

\+ Prueba de vida superada

= IDENTIDAD VERIFICADA

```

Mientras que:

```text
Credencial válida

\+ Rostro no coincidente

= VERIFICACIÓN RECHAZADA

```

O:

```text
Credencial válida

\+ Rostro detectado

\+ Prueba de vida fallida

= POSIBLE INTENTO DE SUPLANTACIÓN

```

Cada proceso será almacenado como una **sesión de verificación**, conservando la identidad ficticia evaluada, factores utilizados, resultados obtenidos, fecha, hora, usuario responsable y decisión final.

Cuando la sesión sea aprobada, podrá asociarse con un trámite notarial ficticio y, posteriormente, enviarse al **Simulador SID-Sunarp**, que representará una integración externa únicamente con fines académicos.

La arquitectura del producto estará organizada conceptualmente en varios componentes:

- gestión de identidades ficticias;

- enrolamiento biométrico;

- credenciales QR/RFID;

- reconocimiento facial;

- prueba de vida;

- motor de reglas;

- sesiones de verificación;

- control de intentos fallidos;

- integridad documental;

- códigos QR de consulta;

- bitácora de auditoría;

- control de acceso;

- Simulador de Identidad;

- Simulador SID-Sunarp.

Esta separación permitirá probar individualmente los módulos y posteriormente evaluar su comportamiento conjunto mediante pruebas de integración y aceptación.

## 4.2 Resumen de capacidades

Las capacidades principales previstas para NotaryVerify son las siguientes:

| **Capacidad**                               | **Descripción**                                                                                                                   |
|---------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| **Gestión de identidades ficticias**        | Registrar, consultar y administrar identidades simuladas utilizadas exclusivamente durante las pruebas del proyecto.              |
| **Enrolamiento biométrico**                 | Registrar muestras faciales autorizadas de participantes voluntarios y asociarlas con identidades ficticias.                      |
| **Lectura de credenciales QR/RFID**         | Utilizar credenciales electrónicas para identificar qué registro debe ser sometido al proceso de verificación.                    |
| **Validación de credenciales**              | Identificar credenciales válidas, inexistentes o revocadas antes de continuar con el proceso.                                     |
| **Reconocimiento facial local**             | Comparar el rostro capturado durante una sesión con la referencia biométrica previamente registrada.                              |
| **Métrica de coincidencia**                 | Producir un resultado de comparación acompañado de una métrica de confianza definida por el mecanismo biométrico implementado.    |
| **Prueba de vida experimental**             | Solicitar desafíos faciales y evaluar si la persona se encuentra presente frente a la cámara.                                     |
| **Verificación multicapa**                  | Combinar los resultados de credencial, reconocimiento facial, prueba de vida y otras reglas antes de producir una decisión final. |
| **Detección de intentos repetidos**         | Registrar verificaciones fallidas y generar alertas cuando se supere el límite configurado.                                       |
| **Sesiones de verificación**                | Conservar de forma estructurada todos los factores utilizados y resultados generados durante una verificación.                    |
| **Gestión de trámites ficticios**           | Asociar una sesión de verificación aprobada con una operación notarial simulada.                                                  |
| **Integridad documental mediante SHA-256**  | Generar y comprobar huellas criptográficas de documentos de prueba para detectar modificaciones posteriores.                      |
| **QR de verificación documental**           | Generar códigos QR que permitan consultar información básica sobre el estado de un documento registrado.                          |
| **Bitácora de auditoría**                   | Registrar eventos críticos realizados dentro del sistema.                                                                         |
| **Encadenamiento criptográfico**            | Relacionar eventos de auditoría con registros anteriores para detectar alteraciones intencionales en el historial protegido.      |
| **Control de acceso basado en roles**       | Restringir operaciones sensibles de configuración, enrolamiento, modificación y auditoría a usuarios autorizados.                 |
| **Simulación de servicios institucionales** | Representar las interacciones necesarias con fuentes externas sin acceder a Reniec ni SID-Sunarp reales.                          |
| **Simulación de errores externos**          | Evaluar escenarios de disponibilidad, rechazo, respuesta incorrecta y tiempo de espera agotado.                                   |
| **Generación de alertas**                   | Informar situaciones como múltiples intentos fallidos, credenciales revocadas o verificaciones sospechosas.                       |
| **Consulta histórica**                      | Permitir revisar sesiones anteriores, factores utilizados, decisiones tomadas y eventos asociados.                                |

Estas capacidades responden directamente a los objetivos de solución definidos en la propuesta del proyecto.

Una característica central del producto es que las capacidades no funcionarán de manera completamente aislada. El valor de NotaryVerify se encuentra precisamente en la combinación de los resultados.

Por ejemplo, el sistema podrá interpretar:

```text
RFID correcto

≠ identidad aprobada automáticamente

```

porque todavía deberán evaluarse el rostro y la prueba de vida.

De igual manera:

```text
Rostro coincidente

≠ identidad aprobada automáticamente

```

si la prueba de vida no ha sido superada.

Este comportamiento representa el principio principal del sistema: **ningún factor aislado debe ser suficiente para considerar aprobada la identidad cuando las reglas configuradas exigen múltiples comprobaciones**.

## 4.3 Suposiciones y dependencias

Para el desarrollo y funcionamiento del prototipo se consideran las siguientes suposiciones:

### Suposiciones

- Se asume que todas las identidades utilizadas durante el proyecto serán ficticias.

- Se asume que los participantes utilizados en pruebas biométricas habrán autorizado expresamente la utilización de sus imágenes.

- Se asume que las pruebas se realizarán dentro de un entorno académico controlado.

- Se asume que los dispositivos de prueba contarán con una cámara funcional para ejecutar reconocimiento facial y prueba de vida.

- Se asume que las credenciales QR/RFID serán creadas específicamente para el prototipo.

- Se asume que una credencial servirá únicamente para identificar el registro que debe verificarse y no para aprobar automáticamente una identidad.

- Se asume que las operaciones notariales utilizadas serán ficticias.

- Se asume que los documentos utilizados durante las pruebas no tendrán valor jurídico.

- Se asume que el sistema contará con usuarios previamente autenticados para ejecutar operaciones restringidas.

- Se asume que los parámetros de comparación facial y prueba de vida serán definidos y evaluados experimentalmente durante el proyecto.

Estas condiciones se desprenden directamente de la delimitación establecida en la propuesta de NotaryVerify.

### Dependencias internas

NotaryVerify tendrá dependencias funcionales entre sus propios componentes.

Por ejemplo:

```text
Credencial

↓

Identidad ficticia

↓

Referencia biométrica

↓

Reconocimiento facial

↓

Liveness

↓

Motor de reglas

↓

Sesión

```

Si no existe una identidad ficticia válida, el sistema no debería continuar con la comparación biométrica correspondiente.

De igual manera, un trámite ficticio no debería ser enviado al Simulador SID-Sunarp cuando la sesión de verificación no haya sido aprobada.

### Dependencias tecnológicas previstas

La propuesta identifica tecnologías de código abierto y ejecución local para los componentes biométricos. Entre las referencias técnicas consideradas se encuentran **OpenCV**, modelos compatibles con reconocimiento facial local y **MediaPipe Face Landmarker** para el análisis de características faciales.

Estas tecnologías son consideradas alternativas previstas para la implementación; la selección definitiva y configuración concreta podrá precisarse durante el diseño e implementación.

### Dependencias externas simuladas

El proyecto contempla principalmente dos servicios externos simulados:

**Simulador de Identidad**

Representará académicamente una fuente externa de identidad y permitirá reproducir situaciones como:

- identidad encontrada;

- identidad inexistente;

- fotografía diferente;

- servicio disponible;

- servicio temporalmente no disponible;

- respuesta incorrecta;

- tiempo de espera agotado.

**Simulador SID-Sunarp**

Representará de manera simplificada el envío de un trámite ficticio después de una verificación aprobada y podrá generar:

- trámite aceptado;

- trámite rechazado;

- servicio no disponible;

- error;

- tiempo de espera agotado.

Estos simuladores son dependencias internas creadas por el propio proyecto y **no constituyen conexiones reales con sistemas gubernamentales**.

### Sistemas que NO constituyen dependencias obligatorias

NotaryVerify no dependerá directamente de:

- Reniec;

- SID-Sunarp real;

- certificados institucionales;

- firma digital gubernamental;

- entidades financieras;

- API biométricas comerciales;

- bases de datos de ciudadanos;

- servicios comerciales de identificación.

Esta decisión permite mantener el proyecto técnicamente viable dentro de un entorno académico y evita la necesidad de credenciales oficiales, información confidencial o servicios de pago.

## 4.4 Licenciamiento e instalación

NotaryVerify será desarrollado como un **prototipo académico**, utilizando principalmente herramientas y tecnologías que permitan realizar el desarrollo y las pruebas sin depender obligatoriamente de servicios comerciales de pago.

La propuesta contempla utilizar tecnologías de código abierto para el reconocimiento facial y análisis de características faciales, incluyendo OpenCV y herramientas compatibles con procesamiento local.

El sistema estará compuesto por una aplicación web y servicios desarrollados para representar las distintas funciones del prototipo. Su instalación deberá contemplar al menos:

- aplicación principal de NotaryVerify;

- backend y servicios internos;

- base de datos utilizada por el prototipo;

- Simulador de Identidad;

- Simulador SID-Sunarp;

- librerías necesarias para reconocimiento facial;

- componentes de prueba de vida;

- configuración de cámara;

- soporte para generación y lectura de códigos QR;

- soporte para los dispositivos RFID utilizados durante las pruebas;

- librerías necesarias para cálculo SHA-256;

- dependencias necesarias para las pruebas automatizadas.

La versión definitiva del procedimiento de instalación deberá documentarse una vez que la arquitectura y las tecnologías hayan sido completamente establecidas durante el desarrollo.

En cuanto al licenciamiento, el README base del proyecto **no define todavía una licencia concreta para NotaryVerify**, por lo que no sería correcto afirmar en el FD02 que el proyecto será MIT, Apache u otra licencia específica sin que esa decisión haya sido tomada.

Por tanto, para el documento puede indicarse:

El proyecto utilizará tecnologías y librerías compatibles con el desarrollo académico y priorizará herramientas de código abierto. La licencia específica del código fuente de NotaryVerify será definida posteriormente por el equipo de desarrollo, verificando previamente la compatibilidad de las licencias correspondientes a las dependencias utilizadas.

Esto es mejor que inventar una licencia solo porque otros proyectos la tienen.

Del mismo modo, la instalación no requerirá conexión directa con infraestructura de Reniec o Sunarp, debido a que dichas integraciones serán representadas mediante servicios simulados desarrollados como parte del propio prototipo.

En conjunto, esta perspectiva permite que NotaryVerify sea desplegado y evaluado como una **plataforma experimental independiente**, enfocada en la verificación multicapa, trazabilidad y pruebas de seguridad, sin asumir capacidades legales o institucionales que están fuera de los objetivos del proyecto.

# 5. Características del producto

NotaryVerify estará compuesto por un conjunto de características funcionales orientadas a ejecutar, controlar y auditar un proceso experimental de verificación multicapa de identidad aplicado a trámites notariales simulados. Cada característica contribuirá a evaluar uno o más factores de seguridad antes de producir una decisión final sobre la sesión de verificación.

La característica central del producto será que **ningún mecanismo individual deberá aprobar por sí solo una identidad cuando las reglas configuradas exijan la validación conjunta de varios factores**. De esta manera, una credencial válida no será suficiente cuando el reconocimiento facial no coincida, y una coincidencia facial tampoco permitirá aprobar la operación cuando la prueba de vida no haya sido superada.

Las principales características previstas son las siguientes.

## 5.1 Gestión de identidades ficticias

El sistema permitirá registrar y administrar identidades creadas exclusivamente para los escenarios académicos del proyecto.

Cada identidad ficticia podrá contener la información mínima necesaria para ejecutar los procesos de prueba, como:

- identificador interno;

- número de documento ficticio;

- nombres y apellidos simulados;

- fotografía de referencia autorizada;

- estado del registro;

- fecha de creación;

- información asociada al enrolamiento biométrico;

- credenciales vinculadas.

Las identidades utilizadas por NotaryVerify no procederán de Reniec ni de otras bases de datos gubernamentales.

Esta información será proporcionada por el **Simulador de Identidad**, que representará únicamente para fines experimentales una fuente externa de consulta.

El sistema deberá permitir distinguir situaciones como:

- identidad existente;

- identidad inexistente;

- identidad activa;

- identidad inhabilitada;

- identidad con información incompleta;

- referencia biométrica no registrada.

Esta característica permitirá ejecutar pruebas de comportamiento sin utilizar información perteneciente a ciudadanos reales.

## 5.2 Enrolamiento biométrico

NotaryVerify permitirá registrar muestras faciales correspondientes exclusivamente a participantes voluntarios que hayan autorizado su utilización dentro del proyecto.

El enrolamiento tendrá como finalidad crear una referencia biométrica que posteriormente pueda ser comparada durante las sesiones de verificación.

El sistema deberá permitir:

- seleccionar una identidad ficticia;

- capturar una o varias muestras faciales;

- comprobar que existe un rostro visible;

- asociar las muestras con el registro seleccionado;

- actualizar el enrolamiento cuando corresponda;

- restringir la modificación biométrica a usuarios autorizados;

- registrar en auditoría las operaciones de creación o modificación del enrolamiento.

La modificación de una referencia biométrica deberá considerarse una operación crítica, debido a que un cambio no autorizado podría alterar el comportamiento futuro de las verificaciones.

Por esta razón, el sistema deberá controlar quién realiza dichas operaciones y dejar evidencia en la bitácora correspondiente.

## 5.3 Gestión de credenciales QR

El sistema permitirá generar y utilizar códigos QR como credenciales de prueba asociadas a identidades ficticias.

El código QR no deberá contener directamente información biométrica ni información personal sensible. En su lugar, contendrá un identificador o token que permita al sistema determinar qué registro interno debe ser consultado.

Al leer la credencial, NotaryVerify deberá comprobar:

- existencia del identificador;

- asociación con una identidad;

- estado de la credencial;

- vigencia lógica establecida por el sistema;

- condición de activa o revocada.

El resultado de esta comprobación podrá ser, por ejemplo:

- **CREDENCIAL VÁLIDA**;

- **CREDENCIAL NO REGISTRADA**;

- **CREDENCIAL REVOCADA**;

- **CREDENCIAL INVÁLIDA**.

Una credencial válida permitirá iniciar o continuar con los siguientes factores de verificación, pero **no aprobará automáticamente la identidad**.

## 5.4 Gestión de credenciales RFID

Como mecanismo alternativo o complementario al código QR, NotaryVerify permitirá utilizar tarjetas o etiquetas RFID asociadas con identidades ficticias.

La finalidad del RFID será equivalente a la del QR: identificar de manera controlada el registro esperado para la sesión.

La lectura deberá recuperar únicamente un identificador asociado con la credencial y permitir al sistema comprobar su estado.

El prototipo permitirá evaluar escenarios como:

- RFID registrado;

- RFID inexistente;

- RFID asignado a otra identidad;

- RFID revocado;

- RFID utilizado correctamente pero con fallo posterior en reconocimiento facial.

De esta forma, se podrá demostrar experimentalmente que **poseer físicamente una credencial no equivale a demostrar la identidad de la persona que la presenta**.

## 5.5 Reconocimiento facial local

NotaryVerify incorporará un mecanismo de reconocimiento facial ejecutado localmente mediante herramientas compatibles con el procesamiento biométrico definido para el proyecto.

Durante la verificación, el sistema capturará el rostro presentado frente a la cámara y realizará una comparación con la referencia previamente asociada a la identidad ficticia.

El componente deberá producir al menos:

- detección del rostro;

- comparación contra la referencia;

- métrica o puntuación obtenida;

- resultado de coincidencia o no coincidencia;

- estado del procesamiento.

La interfaz no deberá obligar al operador a interpretar directamente valores complejos del algoritmo. En su lugar, podrá presentar resultados comprensibles como:

**ROSTRO COINCIDENTE**

o

**ROSTRO NO COINCIDENTE**

acompañados, cuando sea necesario para las pruebas, de la métrica generada por el modelo.

Las métricas obtenidas durante las pruebas permitirán posteriormente analizar aceptación, rechazo, falsos positivos y falsos negativos.

## 5.6 Prueba de vida experimental

El sistema incorporará una prueba de vida destinada a evaluar que el participante se encuentra presente frente a la cámara y dificultar intentos básicos de engaño mediante fotografías estáticas.

La prueba podrá utilizar desafíos seleccionados por el sistema, por ejemplo:

- parpadear;

- girar el rostro hacia una dirección;

- realizar un movimiento facial definido;

- mantener el rostro visible durante la secuencia solicitada.

El desafío deberá ser comunicado al participante y evaluado mediante la información obtenida desde la cámara.

El resultado podrá presentarse como:

**PRUEBA DE VIDA SUPERADA**

o

**PRUEBA DE VIDA FALLIDA**.

El sistema deberá poder registrar qué desafío fue solicitado y qué resultado se obtuvo.

El carácter experimental de este componente deberá mantenerse claramente indicado. Su objetivo será analizar determinados escenarios controlados de presentación de fotografías y no sustituir soluciones biométricas certificadas.

## 5.7 Motor de verificación multicapa

Esta será una de las características principales de NotaryVerify.

El motor de reglas será responsable de recibir los resultados producidos por los distintos mecanismos y generar una decisión global.

Las reglas permitirán establecer condiciones como:

```text
Credencial válida

\+ Rostro coincidente

\+ Prueba de vida superada

= IDENTIDAD VERIFICADA

```


```text
Credencial válida

\+ Rostro no coincidente

= VERIFICACIÓN RECHAZADA

```


```text
Credencial válida

\+ Rostro coincidente

\+ Prueba de vida fallida

= VERIFICACIÓN RECHAZADA

```


```text
Credencial revocada

= VERIFICACIÓN RECHAZADA

```


```text
Múltiples intentos fallidos

= GENERAR ALERTA

```

El motor permitirá centralizar la lógica de decisión evitando que cada módulo determine independientemente la aprobación del proceso.

Además, las reglas deberán poder ser identificadas durante una auditoría para saber cuál de ellas produjo la decisión final.

## 5.8 Gestión de sesiones de verificación

Cada intento de comprobación generará una **sesión de verificación única**.

Esta sesión funcionará como el registro principal que agrupa todas las evidencias generadas durante el proceso.

La sesión podrá contener:

- identificador único;

- identidad ficticia evaluada;

- usuario responsable;

- credencial utilizada;

- tipo de credencial;

- resultado de la validación de credencial;

- resultado del reconocimiento facial;

- métrica facial obtenida;

- resultado de la prueba de vida;

- desafío utilizado;

- reglas ejecutadas;

- alertas generadas;

- fecha;

- hora;

- decisión final.

Los posibles estados generales de una sesión podrán incluir:

- iniciada;

- en proceso;

- aprobada;

- rechazada;

- requiere revisión;

- cancelada;

- error.

La existencia de una sesión permitirá reconstruir posteriormente cómo se tomó una decisión determinada.

## 5.9 Detección de intentos fallidos consecutivos

NotaryVerify registrará los intentos de verificación rechazados para detectar comportamientos repetitivos.

Cuando se alcance el límite configurado por las reglas del proyecto, el sistema deberá producir una alerta.

Por ejemplo:

```text
Intento 1 → RECHAZADO

Intento 2 → RECHAZADO

Intento 3 → RECHAZADO

RESULTADO:

MÚLTIPLES INTENTOS FALLIDOS

ALERTA GENERADA

```

El número definitivo de intentos que genere una alerta deberá mantenerse configurable o establecerse formalmente durante el levantamiento de requerimientos.

La alerta deberá quedar relacionada con la información disponible sobre las sesiones que la originaron.

## 5.10 Gestión de trámites notariales ficticios

NotaryVerify permitirá asociar una sesión de identidad aprobada con un trámite notarial simulado.

La finalidad de esta característica será demostrar que una operación de prueba se encuentra precedida por una determinada verificación de identidad.

Los trámites utilizados no tendrán efectos jurídicos y estarán creados exclusivamente para los escenarios académicos.

El sistema deberá evitar que un trámite continúe hacia las etapas posteriores cuando la sesión relacionada no se encuentre aprobada.

De esta forma podrá cumplirse una condición como:

```text
SESIÓN APROBADA

↓

TRÁMITE HABILITADO

```

mientras que:

```text
SESIÓN RECHAZADA

↓

TRÁMITE BLOQUEADO

```

Esta relación permitirá comprobar mediante pruebas que una decisión negativa de identidad tiene consecuencias funcionales dentro del flujo.

## 5.11 Verificación de integridad documental mediante SHA-256

El sistema permitirá generar una huella criptográfica SHA-256 para los documentos ficticios relacionados con las operaciones realizadas.

Al registrar un documento, NotaryVerify calculará su hash y almacenará el valor obtenido.

Posteriormente podrá volver a calcular la huella del archivo presentado y compararla con el valor registrado originalmente.

Si ambas huellas son iguales:

**DOCUMENTO ÍNTEGRO**

Si son diferentes:

**DOCUMENTO MODIFICADO / INTEGRIDAD NO VÁLIDA**

Esta característica permitirá realizar pruebas deliberadas modificando archivos después de su registro y comprobar si el sistema detecta correctamente las alteraciones.

## 5.12 QR de verificación documental

Los documentos ficticios podrán incorporar un código QR destinado a facilitar su consulta posterior.

El QR no almacenará directamente información personal o biométrica.

Contendrá un identificador que permita consultar dentro de NotaryVerify información como:

- documento registrado;

- estado;

- sesión asociada;

- fecha de registro;

- resultado de comprobación de integridad.

El sistema deberá contemplar respuestas frente a:

- identificador válido;

- identificador inexistente;

- registro revocado;

- documento alterado;

- documento íntegro.

## 5.13 Bitácora de auditoría

NotaryVerify incorporará una bitácora destinada a registrar operaciones relevantes realizadas dentro del sistema.

Entre los eventos que podrán registrarse se encuentran:

- inicio y cierre de sesión;

- creación de identidad ficticia;

- modificación de identidad;

- enrolamiento biométrico;

- modificación de enrolamiento;

- emisión de credencial;

- revocación de credencial;

- inicio de una verificación;

- aprobación o rechazo;

- modificación de reglas;

- generación de alertas;

- registro de documentos;

- interacción con servicios simulados;

- operaciones administrativas.

Los registros podrán incluir:

- identificador de evento;

- usuario responsable;

- fecha y hora;

- tipo de acción;

- entidad afectada;

- resultado;

- información técnica necesaria para auditoría.

La bitácora deberá permitir reconstruir cronológicamente las operaciones realizadas.

## 5.14 Encadenamiento criptográfico de eventos

Como mecanismo complementario de auditoría, determinados eventos críticos serán protegidos mediante encadenamiento criptográfico.

Cada registro protegido podrá incorporar información derivada criptográficamente del evento anterior.

Conceptualmente:

```text
Evento 1

↓

Hash 1

↓

Evento 2 + Hash 1

↓

Hash 2

↓

Evento 3 + Hash 2

```

Si un evento anterior fuera modificado intencionalmente, la cadena posterior dejaría de ser consistente.

NotaryVerify deberá disponer de una función que permita comprobar dicha integridad y producir un resultado indicando si la cadena de registros protegidos mantiene su consistencia.

Esta característica no pretende convertir la aplicación en una blockchain, sino utilizar principios de encadenamiento criptográfico para experimentar con la detección de modificaciones realizadas sobre un historial de auditoría.

## 5.15 Control de acceso basado en roles

El sistema deberá autenticar a los usuarios que requieran acceso a sus funcionalidades internas y restringir las operaciones según el rol asignado.

Inicialmente se contemplan los siguientes perfiles:

- **Operador de verificación**;

- **Administrador**;

- **Auditor / Supervisor**.

El operador podrá ejecutar las verificaciones correspondientes, mientras que el administrador tendrá acceso a las funciones de configuración y gestión.

El auditor estará principalmente orientado a la consulta de información, sesiones, alertas y registros históricos.

Las operaciones críticas deberán impedirse cuando el usuario autenticado no disponga del rol correspondiente.

La propuesta del proyecto establece como meta que el **100 % de las operaciones críticas relacionadas con configuración, enrolamiento, modificación y auditoría estén restringidas a usuarios autorizados**.

## 5.16 Simulador de Identidad

El producto incluirá un servicio propio que representará académicamente una fuente externa de identidad.

El Simulador de Identidad permitirá experimentar con diferentes respuestas sin acceder a Reniec.

Entre los escenarios previstos se encuentran:

- identidad encontrada;

- identidad inexistente;

- registro activo;

- registro inactivo;

- fotografía de referencia diferente;

- servicio disponible;

- servicio no disponible;

- respuesta incorrecta;

- tiempo de espera agotado.

NotaryVerify deberá interpretar cada respuesta y actuar según las reglas establecidas.

Esto permitirá probar tanto los casos exitosos como las condiciones de error de integración.

## 5.17 Simulador SID-Sunarp

NotaryVerify también incluirá un componente destinado a representar de forma simplificada una integración posterior con un servicio institucional.

El **Simulador SID-Sunarp** no reproducirá completamente las funcionalidades del SID-Sunarp oficial.

Su finalidad será permitir demostrar que un trámite ficticio solo puede ser enviado cuando la sesión de identidad correspondiente haya sido aprobada.

Podrá devolver respuestas como:

- trámite aceptado;

- trámite rechazado;

- servicio no disponible;

- error de procesamiento;

- tiempo de espera agotado.

Esta característica permitirá realizar pruebas de integración y validar el comportamiento del sistema cuando una dependencia externa falla.

## 5.18 Generación y gestión de alertas

El sistema deberá producir alertas frente a situaciones que requieran atención adicional.

Entre los eventos que pueden originarlas se contemplan:

- múltiples intentos fallidos;

- utilización de una credencial revocada;

- modificación biométrica sensible;

- comportamiento inconsistente durante una verificación;

- errores críticos de integración;

- alteración detectada en registros protegidos.

Cada alerta deberá conservar información suficiente para conocer:

- qué evento la generó;

- cuándo ocurrió;

- qué usuario estaba involucrado;

- qué sesión se encontraba relacionada;

- estado actual de la alerta.

## 5.19 Consulta histórica y trazabilidad

Los usuarios autorizados podrán consultar verificaciones ejecutadas anteriormente.

La consulta deberá permitir reconstruir la secuencia completa de una sesión:

```text
IDENTIDAD CONSULTADA

↓

CREDENCIAL UTILIZADA

↓

RECONOCIMIENTO FACIAL

↓

PRUEBA DE VIDA

↓

REGLAS APLICADAS

↓

DECISIÓN

↓

EVENTOS DE AUDITORÍA

```

Esta característica permitirá que NotaryVerify no entregue únicamente una decisión final, sino evidencia suficiente para analizar posteriormente cómo fue obtenida.

## 5.20 Característica experimental y de evaluación

NotaryVerify será diseñado no solamente para ejecutar verificaciones, sino también para poder **evaluar el comportamiento de los mecanismos implementados**.

El proyecto contempla como parte de su validación la realización de al menos **100 intentos biométricos controlados**, distribuidos entre usuarios legítimos y escenarios de suplantación.

Los resultados permitirán registrar y analizar:

- aceptaciones correctas;

- rechazos correctos;

- falsos positivos;

- falsos negativos;

- resultado de prueba de vida;

- comportamiento frente a fotografías;

- comportamiento frente a credenciales inválidas;

- respuesta ante documentos modificados;

- respuesta ante fallos de servicios simulados.

Esta característica experimental es fundamental porque permitirá que la efectividad de NotaryVerify no se argumente únicamente a partir de que “el sistema funciona”, sino mediante evidencia obtenida durante las pruebas realizadas sobre el prototipo.

En conjunto, estas características permitirán que NotaryVerify funcione como un **entorno experimental integral de verificación multicapa, detección de escenarios de suplantación, trazabilidad y auditoría**, manteniendo siempre la delimitación de que los resultados obtenidos pertenecen exclusivamente al prototipo académico y no representan una identificación oficial o legal.

# 6. Restricciones

NotaryVerify será desarrollado bajo un conjunto de restricciones técnicas, operativas, legales, académicas y de seguridad que delimitan el alcance real del prototipo y condicionan determinadas decisiones de implementación. Estas restricciones son necesarias para mantener la viabilidad del proyecto dentro del ciclo académico y, al mismo tiempo, evitar que el sistema sea presentado como una solución oficial de identificación.

## 6.1 Restricciones académicas

El proyecto será desarrollado como un **prototipo académico experimental** dentro del curso de Calidad y Pruebas de Software. Por este motivo, su objetivo principal será demostrar, analizar y evaluar el comportamiento de mecanismos de verificación multicapa de identidad en escenarios controlados.

Los resultados obtenidos no tendrán valor de identificación legal ni podrán ser utilizados para autorizar actos notariales reales.

Cuando NotaryVerify muestre un resultado como:

**IDENTIDAD VERIFICADA**

dicho resultado significará únicamente que la persona evaluada superó satisfactoriamente los controles experimentales configurados en el prototipo.

La identificación legal continuará dependiendo de los procedimientos, sistemas y autoridades oficialmente habilitados.

## 6.2 Restricciones sobre información real

NotaryVerify no utilizará información perteneciente a clientes reales de una notaría.

Las pruebas deberán realizarse exclusivamente con:

- identidades ficticias;

- números de documento ficticios;

- trámites notariales simulados;

- documentos creados específicamente para pruebas;

- muestras biométricas pertenecientes a participantes voluntarios autorizados.

No se deberán utilizar fotografías de ciudadanos obtenidas desde Internet ni información biométrica procedente de fuentes públicas sin consentimiento.

La base de datos académica deberá estar compuesta únicamente por información creada específicamente para el proyecto.

## 6.3 Restricciones biométricas

El reconocimiento facial y la prueba de vida implementados tendrán carácter experimental.

El sistema no será certificado como solución biométrica oficial.

El comportamiento del reconocimiento facial podrá verse afectado por condiciones como:

- iluminación;

- posición del rostro;

- calidad de la cámara;

- resolución de la imagen;

- presencia de elementos que cubran parcialmente el rostro;

- distancia respecto a la cámara;

- movimiento;

- calidad de las muestras utilizadas durante el enrolamiento.

Por este motivo, los resultados deberán ser evaluados durante las pruebas y no asumirse como completamente infalibles.

Asimismo, los umbrales utilizados para determinar coincidencia facial serán establecidos experimentalmente y deberán documentarse.

## 6.4 Restricciones de la prueba de vida

La prueba de vida estará diseñada para experimentar principalmente con ataques básicos mediante fotografías impresas o fotografías mostradas desde pantallas.

No se garantizará la detección de técnicas avanzadas como:

- deepfakes sofisticados;

- máscaras tridimensionales;

- reproducción avanzada de video;

- ataques biométricos especializados;

- inyección directa de video a nivel de hardware o sistema operativo.

Estas técnicas quedan fuera del alcance inicial debido a la complejidad técnica y al carácter académico del proyecto.

La prueba de vida no deberá presentarse como equivalente a soluciones certificadas utilizadas por entidades financieras o gubernamentales.

## 6.5 Restricciones respecto a Reniec

NotaryVerify no tendrá acceso directo a:

- bases de datos de Reniec;

- fotografías oficiales;

- servicios biométricos institucionales;

- información personal de ciudadanos;

- API privadas o institucionales de Reniec.

Toda interacción necesaria con información de identidad será representada mediante el **Simulador de Identidad** desarrollado por el propio equipo.

## 6.6 Restricciones respecto a SID-Sunarp

NotaryVerify no realizará operaciones reales sobre SID-Sunarp.

No tendrá acceso a:

- credenciales institucionales;

- certificados oficiales;

- documentos notariales reales;

- infraestructura interna de Sunarp;

- servicios privados del SID-Sunarp.

La integración será representada mediante el **Simulador SID-Sunarp**, creado específicamente para reproducir determinados escenarios de integración.

## 6.7 Restricciones de las credenciales QR

Los códigos QR utilizados dentro de NotaryVerify no deberán almacenar directamente:

- fotografías biométricas;

- nombres completos cuando no sea necesario;

- números reales de documentos;

- plantillas biométricas;

- información personal sensible.

El QR deberá contener únicamente un identificador o token que permita consultar el registro interno correspondiente.

La posesión de un QR válido no podrá ser utilizada por sí sola para aprobar una identidad.

## 6.8 Restricciones de RFID

Las credenciales RFID utilizadas serán exclusivamente dispositivos de prueba.

La lectura de una tarjeta RFID deberá permitir únicamente recuperar un identificador asociado al registro interno correspondiente.

Una tarjeta RFID válida no deberá producir automáticamente una verificación aprobada.

El proceso deberá continuar con los demás factores configurados, especialmente reconocimiento facial y prueba de vida.

## 6.9 Restricciones sobre documentos

Los documentos utilizados dentro del proyecto serán ficticios y carecerán de validez jurídica.

El sistema podrá comprobar su integridad mediante SHA-256, pero esta función no deberá interpretarse como una firma digital oficial.

El cálculo de una huella SHA-256 permite detectar modificaciones del contenido, pero no certifica jurídicamente quién creó o firmó un documento.

## 6.10 Restricciones técnicas

La ejecución de las funcionalidades biométricas requerirá:

- cámara compatible;

- permisos de acceso a cámara;

- navegador compatible con las funciones implementadas;

- recursos mínimos suficientes para ejecutar los algoritmos utilizados;

- librerías instaladas correctamente.

El sistema dependerá también de la correcta disponibilidad de la base de datos y de los servicios internos del prototipo.

## 6.11 Restricciones de conectividad

Algunas funcionalidades podrán depender de la comunicación entre frontend, backend y servicios simulados.

Cuando alguno de estos servicios no se encuentre disponible, el sistema deberá manejar adecuadamente el error y evitar aprobar una operación únicamente porque no pudo completar una validación.

## 6.12 Restricción temporal

El alcance funcional deberá mantenerse viable dentro del ciclo académico.

Por esta razón, se priorizarán las funcionalidades directamente relacionadas con:

- verificación de identidad;

- biometría;

- prueba de vida;

- reglas multicapa;

- trazabilidad;

- integridad;

- auditoría;

- pruebas.

Las funcionalidades adicionales que no contribuyan directamente al objetivo central podrán ser consideradas de prioridad media o baja.

# 7. Rangos de calidad

Los rangos de calidad establecen criterios generales que permitirán determinar cuándo el comportamiento de NotaryVerify puede considerarse aceptable o inadecuado.

Estos rangos servirán posteriormente como referencia para la definición de requisitos no funcionales, criterios de aceptación y casos de prueba.

## 7.1 Funcionalidad

### Rango bajo

Se considerará que el sistema presenta un rango bajo de funcionalidad cuando:

- no pueda completar correctamente el proceso de verificación;

- apruebe una identidad aun cuando uno de los factores críticos haya fallado;

- no registre correctamente las sesiones;

- permita utilizar credenciales revocadas;

- no detecte documentos deliberadamente modificados;

- permita enviar trámites simulados sin una sesión aprobada;

- no respete los permisos definidos por rol.

### Rango aceptable

Se considerará aceptable cuando:

- el flujo principal pueda completarse correctamente;

- las reglas multicapa sean aplicadas;

- cada factor genere un resultado identificable;

- las sesiones sean almacenadas correctamente;

- los controles de acceso funcionen conforme a los roles establecidos;

- las operaciones críticas puedan ser auditadas.

### Rango alto

Se considerará alto cuando, además de cumplir lo anterior:

- exista trazabilidad completa entre identidad, credencial, biometría, prueba de vida, decisión y auditoría;

- los escenarios de error sean gestionados adecuadamente;

- las operaciones críticas estén protegidas;

- el sistema permita reconstruir completamente el proceso realizado.

## 7.2 Precisión biométrica

El módulo de reconocimiento facial deberá ser evaluado mediante intentos controlados.

La propuesta establece la ejecución de al menos **100 intentos**, distribuidos entre usuarios legítimos y escenarios de suplantación.

### Rango bajo

Existencia frecuente de:

- aceptaciones incorrectas;

- rechazos incorrectos;

- resultados inconsistentes;

- grandes variaciones ante condiciones similares.

### Rango aceptable

El sistema permite distinguir razonablemente entre usuarios legítimos y personas diferentes, manteniendo tasas documentadas de aceptación y rechazo.

### Rango alto

El sistema presenta resultados consistentes bajo las condiciones controladas definidas y mantiene tasas reducidas de falsos positivos y falsos negativos.

Los valores exactos serán establecidos después de la ejecución de las pruebas experimentales y no deberán inventarse antes de disponer de evidencia.

## 7.3 Prueba de vida

### Rango bajo

El sistema:

- acepta fotografías estáticas de manera frecuente;

- no detecta correctamente los desafíos solicitados;

- presenta resultados inconsistentes.

### Rango aceptable

La prueba permite diferenciar, dentro de los escenarios controlados, entre una persona real realizando el desafío y una fotografía estática.

### Rango alto

La prueba responde correctamente en la mayoría de los escenarios definidos y mantiene trazabilidad sobre:

- desafío solicitado;

- resultado;

- tiempo de ejecución;

- decisión.

## 7.4 Integridad documental

### Rango bajo

El sistema no detecta modificaciones deliberadas en los documentos utilizados durante las pruebas.

### Rango aceptable

El sistema detecta correctamente las modificaciones mediante comparación SHA-256.

### Rango alto

Se logra detectar el **100 % de los documentos deliberadamente modificados incluidos en el conjunto de pruebas controladas**, conforme al objetivo planteado en el proyecto.

## 7.5 Seguridad y control de acceso

### Rango bajo

Usuarios sin autorización pueden:

- modificar identidades;

- realizar enrolamientos;

- revocar credenciales;

- modificar reglas;

- acceder a operaciones administrativas.

### Rango aceptable

Las operaciones críticas se encuentran protegidas de acuerdo con el rol asignado.

### Rango alto

El **100 % de las operaciones críticas de configuración, enrolamiento, modificación y auditoría** se encuentran restringidas a usuarios autorizados y las acciones realizadas quedan registradas.

## 7.6 Trazabilidad

### Rango bajo

La decisión final no puede relacionarse claramente con los factores que la originaron.

### Rango aceptable

Cada sesión permite conocer:

- identidad;

- credencial;

- factores;

- resultados;

- usuario;

- fecha y hora;

- decisión.

### Rango alto

El sistema permite reconstruir completamente el proceso y mantiene trazabilidad entre:

```text
Necesidad

↓

Requerimiento

↓

Funcionalidad

↓

Caso de prueba

↓

Resultado

```

El proyecto plantea alcanzar trazabilidad del **100 % de los requerimientos de prioridad alta con sus respectivos casos de prueba**.

## 7.7 Rendimiento

### Rango bajo

Se considerará bajo cuando:

- las operaciones normales generen esperas prolongadas;

- la interfaz deje de responder;

- el procesamiento facial impida continuar de manera razonable;

- las respuestas de servicios internos presenten bloqueos frecuentes.

### Rango aceptable

Las operaciones se completan dentro de tiempos adecuados para la demostración del prototipo sin bloquear innecesariamente al usuario.

### Rango alto

Los módulos críticos presentan tiempos estables, documentados y reproducibles bajo condiciones de prueba controladas.

Los límites exactos en segundos deberán definirse después de realizar mediciones iniciales sobre el hardware utilizado en el proyecto.

## 7.8 Usabilidad

### Rango bajo

El usuario necesita conocer detalles técnicos de biometría o criptografía para interpretar el sistema.

### Rango aceptable

La interfaz presenta mensajes comprensibles como:

- Credencial válida;

- Rostro coincidente;

- Prueba de vida superada;

- Verificación rechazada;

- Requiere revisión.

### Rango alto

Además de presentar mensajes claros, el sistema guía al operador durante cada etapa y permite identificar fácilmente qué factor provocó un rechazo.

## 7.9 Confiabilidad

### Rango bajo

El mismo escenario produce resultados arbitrariamente diferentes sin una causa identificable.

### Rango aceptable

El sistema mantiene un comportamiento consistente bajo condiciones equivalentes.

### Rango alto

Además de ser consistente, registra correctamente errores, excepciones, decisiones y fallos de integración sin perder la trazabilidad de las operaciones.

## 7.10 Calidad de las pruebas

NotaryVerify deberá disponer de pruebas automatizadas y manuales sobre los módulos críticos.

La propuesta establece como objetivo una cobertura automatizada igual o superior al **80 % en los componentes seleccionados**.

Asimismo, deberán ejecutarse:

- pruebas unitarias;

- pruebas de integración;

- pruebas de interfaz;

- pruebas de aceptación;

- pruebas exploratorias;

- pruebas de seguridad;

- pruebas de rendimiento.

Al momento de la entrega final se establece como objetivo mantener **cero defectos críticos abiertos**.

# 8. Precedencia y Prioridad

Las funcionalidades de NotaryVerify serán clasificadas según su importancia para alcanzar el objetivo principal del proyecto.

La prioridad considera principalmente el impacto de una funcionalidad sobre la verificación de identidad, la seguridad, la trazabilidad y la posibilidad de realizar pruebas significativas.

## 8.1 Alta prioridad

### RF01 – Gestión de identidades ficticias

Constituye la base sobre la que se realizarán las verificaciones y permite mantener el proyecto independiente de información real.

### RF02 – Enrolamiento biométrico

Es necesario para disponer de referencias faciales controladas contra las cuales realizar las comparaciones.

### RF03 – Validación de credenciales QR/RFID

Permite identificar el registro esperado antes de iniciar la verificación biométrica.

### RF04 – Reconocimiento facial

Representa uno de los factores centrales de comprobación de identidad.

### RF05 – Prueba de vida

Es fundamental para evaluar escenarios básicos de presentación de fotografías o intentos de engaño.

### RF06 – Motor de reglas multicapa

Es una de las funcionalidades de mayor prioridad, debido a que representa el principio central de NotaryVerify: evitar que un único factor determine la aprobación.

### RF07 – Sesiones de verificación

Permite conservar el resultado completo de cada proceso y mantener trazabilidad.

### RF08 – Detección de intentos fallidos

Contribuye a identificar comportamientos repetitivos y generar alertas.

### RF09 – Integridad mediante SHA-256

Permite comprobar modificaciones realizadas sobre documentos asociados con operaciones verificadas.

### RF11 – Bitácora de auditoría

Es necesaria para reconstruir operaciones y analizar posteriormente los eventos realizados.

### RF12 – Integración con simuladores

Permite ejecutar el proyecto sin depender de Reniec o SID-Sunarp reales.

### RF14 – Autenticación y roles

Es indispensable para impedir accesos no autorizados a funcionalidades críticas.

### RF15 – Consulta de sesiones y trazabilidad

Permite revisar y demostrar posteriormente cómo se obtuvo cada resultado.

### RF17 – Bloqueo de trámites no autorizados

Garantiza que una operación ficticia no pueda continuar hacia el Simulador SID-Sunarp si la identidad no ha sido previamente aprobada.

## 8.2 Prioridad media

### RF10 – QR de consulta documental

Es importante como mecanismo de verificación posterior, pero no constituye el núcleo del proceso biométrico.

### RF13 – Simulación avanzada de fallos externos

Es importante para pruebas de integración, aunque el funcionamiento básico de los servicios simulados debe implementarse primero.

### RF16 – Asociación con trámites notariales ficticios

Permite demostrar un flujo más completo del producto, aunque depende directamente de que la verificación de identidad ya se encuentre funcional.

## 8.3 Orden general de implementación

La precedencia funcional recomendada será:

```text
1. Usuarios y roles

↓

2\. Identidades ficticias

↓

3\. Enrolamiento biométrico

↓

4\. Credenciales QR/RFID

↓

5\. Reconocimiento facial

↓

6\. Prueba de vida

↓

7\. Motor multicapa

↓

8\. Sesiones

↓

9\. Alertas

↓

10\. Auditoría

↓

11\. Integridad documental

↓

12\. Trámites ficticios

↓

13\. Simulador SID-Sunarp

↓

14\. Pruebas integrales

```

Esta secuencia reduce dependencias innecesarias, ya que las funcionalidades posteriores requieren información generada por los módulos anteriores.

# 9. Otros requerimientos del producto

Además de los requerimientos funcionales, NotaryVerify deberá cumplir un conjunto de condiciones relacionadas con privacidad, seguridad, interoperabilidad, calidad y operación.

## 9.1 Estándares legales y de privacidad

El proyecto deberá considerar la normativa peruana aplicable al tratamiento de información personal y biométrica.

Se tomará como referencia el **Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales**, aprobado mediante Decreto Supremo N.° 016-2024-JUS, debido a que los datos biométricos requieren especial consideración por su sensibilidad.

Por esta razón:

- no se utilizarán datos reales de clientes notariales;

- las identidades serán ficticias;

- los números de documento serán simulados;

- las muestras biométricas corresponderán únicamente a participantes voluntarios;

- deberá existir autorización para su utilización;

- su utilización quedará limitada al proyecto académico;

- no deberán almacenarse datos biométricos dentro de QR o RFID.

## 9.2 Confidencialidad

La información sensible utilizada durante las pruebas deberá estar disponible únicamente para usuarios autorizados.

El sistema deberá evitar mostrar datos innecesarios cuando una funcionalidad pueda realizarse utilizando únicamente identificadores internos.

## 9.3 Autenticación

Las funcionalidades internas deberán requerir autenticación cuando correspondan a operaciones restringidas.

Las credenciales utilizadas para acceder al sistema deberán gestionarse separadamente de las credenciales QR/RFID utilizadas para representar identidades ficticias.

## 9.4 Autorización

NotaryVerify utilizará un modelo basado en roles.

Como mínimo:

- operador;

- administrador;

- auditor/supervisor.

Cada rol deberá disponer únicamente de los permisos necesarios.

## 9.5 Estándares de comunicación

La comunicación entre los componentes deberá utilizar mecanismos estructurados.

Cuando se utilicen servicios internos o simulados, se priorizará:

- API REST;

- HTTP/HTTPS;

- JSON.

En un entorno desplegado, deberá priorizarse HTTPS cuando exista transmisión de información sensible.

## 9.6 Estándares de integración

Los simuladores deberán presentar interfaces suficientemente similares a un servicio externo para permitir realizar pruebas de integración.

Se deberán contemplar respuestas como:

- éxito;

- rechazo;

- error;

- indisponibilidad;

- timeout;

- respuesta inválida.

## 9.7 Estándares de seguridad biométrica

Las muestras biométricas no deberán utilizarse fuera de los objetivos establecidos.

El proyecto deberá mantener una separación clara entre:

**identidad ficticia**

y

**participante voluntario real**.

La identidad dentro de la base de pruebas será ficticia aunque la muestra facial pertenezca a una persona voluntaria.

## 9.8 Integridad

Los documentos de prueba deberán poder ser validados utilizando SHA-256.

La integridad de determinados registros de auditoría deberá poder verificarse mediante encadenamiento criptográfico.

## 9.9 Registro de auditoría

Las operaciones críticas deberán producir evidencia suficiente para determinar posteriormente:

- quién realizó la acción;

- cuándo;

- qué operación realizó;

- sobre qué elemento;

- qué resultado produjo.

## 9.10 Manejo de errores

El sistema deberá evitar que los fallos técnicos produzcan aprobaciones incorrectas.

Por ejemplo:

```text
Servicio de identidad no disponible

≠ Identidad aprobada

```


```text
Error de reconocimiento facial

≠ Rostro coincidente

```


```text
Prueba de vida no completada

≠ Prueba superada

```

En situaciones donde un factor crítico no pueda ser evaluado, el sistema deberá detener el proceso, rechazarlo o enviarlo a revisión según las reglas definidas.

## 9.11 Compatibilidad

La aplicación web deberá estar orientada a navegadores modernos.

La compatibilidad definitiva deberá validarse sobre los navegadores seleccionados durante el desarrollo.

## 9.12 Requerimientos de hardware

Para ejecutar la verificación biométrica será necesario disponer de:

- computadora o laptop;

- cámara compatible;

- lector o mecanismo de lectura QR;

- lector RFID cuando se pruebe este tipo de credencial;

- conectividad suficiente para acceder a los componentes desplegados.

## 9.13 Requerimientos de software

La aplicación requerirá las librerías y tecnologías seleccionadas durante la implementación.

Entre las tecnologías previstas se encuentran herramientas de procesamiento biométrico local como OpenCV y MediaPipe, aunque la configuración definitiva deberá documentarse una vez finalizada la selección tecnológica.

## 9.14 Requerimientos de pruebas

Los requerimientos clasificados como prioridad alta deberán disponer de criterios de aceptación verificables.

Al finalizar el proyecto deberá existir trazabilidad entre el **100 % de los requerimientos de prioridad alta y sus respectivos casos de prueba**.

Además, deberán ejecutarse pruebas:

- unitarias;

- integración;

- interfaz;

- aceptación;

- exploratorias;

- seguridad;

- rendimiento.

## 9.15 Cobertura de pruebas automatizadas

Se establece como objetivo alcanzar una cobertura igual o superior al **80 % en los componentes seleccionados de lógica crítica**.

La cobertura no deberá interpretarse como garantía absoluta de ausencia de defectos, sino como una métrica complementaria de calidad.

## 9.16 Gestión de defectos

Los defectos encontrados deberán ser registrados, clasificados y tratados según su severidad.

Al momento de la entrega final se establece como objetivo:

**0 defectos críticos abiertos.**

Los defectos de menor severidad podrán documentarse como limitaciones conocidas cuando su solución exceda el alcance del proyecto.

## 9.17 Requerimientos de rendimiento

Las operaciones críticas deberán ser sometidas a mediciones de tiempo.

Se deberán analizar como mínimo:

- consulta de identidad;

- lectura de credencial;

- comparación facial;

- prueba de vida;

- generación de decisión;

- consulta histórica;

- validación documental.

Los valores máximos aceptables deberán definirse después de obtener mediciones preliminares sobre el hardware real del proyecto.

## 9.18 Requerimientos de usabilidad

La interfaz deberá comunicar los resultados en términos comprensibles para usuarios que no posean conocimientos avanzados de biometría.

Por ejemplo:

**CREDENCIAL VÁLIDA**

**ROSTRO NO COINCIDENTE**

**PRUEBA DE VIDA FALLIDA**

**VERIFICACIÓN RECHAZADA**

En caso de error, deberá indicarse qué etapa impidió continuar con el proceso.

## 9.19 Requerimientos de trazabilidad

Todas las sesiones deberán conservar suficiente información para reconstruir la secuencia de verificación.

La trazabilidad deberá relacionar:

```text
Usuario

↓

Identidad

↓

Credencial

↓

Reconocimiento facial

↓

Prueba de vida

↓

Reglas aplicadas

↓

Decisión

↓

Trámite ficticio

↓

Auditoría

##
```

9.20 Restricción de validez legal

Toda interfaz, documentación y demostración del prototipo deberá evitar presentar NotaryVerify como mecanismo de certificación oficial.

El sistema deberá mantener claramente la condición de:

**PROTOTIPO ACADÉMICO EXPERIMENTAL**

y sus resultados deberán interpretarse únicamente dentro de los escenarios controlados del proyecto.

# CONCLUSIONES

1.  El Documento de Visión permitió establecer de manera estructurada el propósito, alcance, usuarios, interesados, características, restricciones y principales necesidades de **NotaryVerify – Sistema Experimental de Verificación de Identidad para Trámites Notariales**, delimitando claramente que el proyecto corresponde a un prototipo académico orientado a evaluar mecanismos complementarios de verificación y no a sustituir los procedimientos oficiales de identificación utilizados por las notarías, Reniec o Sunarp.

2.  La propuesta del sistema se encuentra centrada en el problema de los intentos de suplantación de identidad dentro de escenarios notariales simulados y plantea como principio fundamental que la aprobación de una identidad no dependa de un único mecanismo. Para ello, NotaryVerify integrará credenciales QR/RFID, reconocimiento facial local, prueba de vida, reglas multicapa, control de intentos fallidos, sesiones de verificación, integridad documental y auditoría.

3.  La definición de los interesados y usuarios permitió diferenciar correctamente a quienes participan directamente en la operación del prototipo de aquellos que poseen interés en sus resultados. Se establecieron como perfiles principales el operador de verificación, administrador, auditor o supervisor y participante voluntario, junto con servicios externos simulados que permitirán evaluar escenarios de integración sin utilizar sistemas institucionales reales.

4.  Las necesidades identificadas fueron relacionadas inicialmente con requerimientos funcionales, estableciendo una base de trazabilidad que posteriormente podrá desarrollarse con mayor profundidad en el Documento de Especificación de Requerimientos. Esta relación permitirá mantener coherencia entre las necesidades de los usuarios, funcionalidades implementadas y casos de prueba utilizados para validar el sistema.

5.  La vista general del producto permitió establecer una arquitectura conceptual basada en componentes independientes pero relacionados, entre los que se encuentran la gestión de identidades ficticias, enrolamiento biométrico, credenciales, reconocimiento facial, prueba de vida, motor de reglas, sesiones, integridad documental, auditoría y servicios institucionales simulados. Esta separación facilitará posteriormente la realización de pruebas unitarias, de integración y de aceptación sobre los distintos módulos.

6.  La definición de características del producto evidencia que NotaryVerify no será únicamente un sistema de reconocimiento facial, sino un entorno experimental de **verificación multicapa**, en el cual los resultados de distintos mecanismos serán combinados mediante reglas antes de producir una decisión final. Esta característica constituye uno de los principales elementos diferenciadores del proyecto.

7.  Las restricciones establecidas permiten mantener el proyecto dentro de límites técnicos, legales y académicos realistas. Se determinó que no se emplearán datos personales pertenecientes a clientes reales de notarías, fotografías obtenidas de Internet, conexiones reales con Reniec o SID-Sunarp ni certificados institucionales oficiales. Las pruebas serán realizadas mediante identidades ficticias y datos biométricos de participantes voluntarios autorizados.

8.  El tratamiento de información biométrica constituye uno de los aspectos que requieren mayor consideración dentro del proyecto. La Ley N.° 29733 tiene como objeto proteger los datos personales y su nuevo Reglamento fue aprobado mediante el Decreto Supremo N.° 016-2024-JUS, por lo que el prototipo deberá mantener medidas de protección acordes con su naturaleza académica y limitar el tratamiento de las muestras biométricas al propósito expresamente definido.

9.  La utilización de simuladores institucionales constituye una decisión relevante para la viabilidad del proyecto. El **Simulador de Identidad** permitirá representar consultas de registros ficticios, mientras que el **Simulador SID-Sunarp** permitirá evaluar escenarios de aceptación, rechazo, indisponibilidad y error sin utilizar credenciales ni infraestructura gubernamental real. Esto resulta especialmente importante considerando que SID-Sunarp constituye actualmente un mecanismo oficial de presentación electrónica de partes y solicitudes notariales con firma digital para los actos comprendidos por su normativa.

10. Los criterios de calidad definidos permitirán que la evaluación del proyecto no se limite a verificar la existencia de funcionalidades. La propuesta contempla métricas y evidencias como al menos 100 intentos biométricos controlados, evaluación de falsos positivos y falsos negativos, pruebas frente a fotografías, detección de documentos alterados, cobertura automatizada objetivo igual o superior al 80 % en componentes seleccionados, trazabilidad del 100 % de los requerimientos de prioridad alta y cero defectos críticos abiertos al momento de la entrega final.

11. En consecuencia, el Documento de Visión proporciona una base suficientemente definida para continuar con las siguientes etapas del proyecto, principalmente la especificación formal de requerimientos, diseño de arquitectura, implementación, elaboración de escenarios de prueba y validación experimental de los mecanismos propuestos.

# RECOMENDACIONES

1.  Mantener durante todo el desarrollo la delimitación establecida en el Documento de Visión, evitando incorporar funcionalidades que conviertan el proyecto en un sistema general de gestión notarial y priorizando las características relacionadas directamente con verificación de identidad, detección de suplantación, integridad y auditoría.

2.  Mantener consistencia entre los códigos de necesidades y requerimientos definidos en el FD02 y los requerimientos que serán desarrollados posteriormente en el FD03, evitando modificar arbitrariamente la numeración o significado de RF01, RF02, RF03 y los demás requerimientos ya identificados.

3.  Definir criterios de aceptación medibles para cada requerimiento de prioridad alta antes de iniciar las pruebas formales del sistema. Esto permitirá determinar objetivamente si una funcionalidad se considera aprobada o rechazada.

4.  Documentar expresamente los parámetros utilizados por el módulo biométrico, como modelo empleado, umbral de similitud, condiciones de captura y procedimiento de enrolamiento, debido a que estos elementos influirán directamente sobre los resultados de falsos positivos y falsos negativos.

5.  No establecer anticipadamente porcentajes de precisión del reconocimiento facial sin haber realizado las pruebas correspondientes. Los resultados deberán obtenerse experimentalmente mediante el conjunto de intentos definidos para el proyecto.

6.  Realizar las pruebas biométricas bajo condiciones controladas y documentar variables relevantes como iluminación, cámara utilizada, posición del participante y tipo de escenario ejecutado, con la finalidad de que los resultados puedan ser interpretados y reproducidos adecuadamente.

7.  Mantener la prueba de vida claramente identificada como **experimental**, evitando presentarla como equivalente a mecanismos biométricos certificados. Se recomienda evaluar de forma separada los escenarios con persona real, fotografía impresa y fotografía mostrada desde una pantalla.

8.  Aplicar el principio de mínima información en las credenciales QR y RFID, almacenando únicamente identificadores o tokens y evitando incluir directamente fotografías, plantillas biométricas u otra información sensible.

9.  Implementar desde etapas tempranas el control de acceso basado en roles, debido a que operaciones como enrolamiento biométrico, modificación de identidades, revocación de credenciales y configuración de reglas representan acciones sensibles y deben mantenerse restringidas a usuarios autorizados.

10. Incorporar la bitácora de auditoría desde las primeras versiones funcionales del sistema y no únicamente al finalizar el desarrollo, ya que esto permitirá conservar evidencia de las operaciones ejecutadas durante las propias pruebas.

11. Implementar pruebas unitarias de manera progresiva durante el desarrollo, priorizando el motor de reglas, validación de credenciales, control de acceso, integridad SHA-256, manejo de sesiones y lógica de los servicios simulados antes de intentar alcanzar la cobertura objetivo del 80 %.

12. Diseñar escenarios de integración negativos además de los casos exitosos. Los simuladores deberían permitir probar indisponibilidad, timeout, respuesta inválida, identidad inexistente y rechazo, verificando que ninguno de estos casos provoque una aprobación incorrecta.

13. Mantener separados los conceptos de **integridad mediante SHA-256** y **firma digital**, debido a que el hash permitirá verificar modificaciones en los documentos de prueba, pero no proporcionará por sí mismo autenticidad jurídica ni reemplazará certificados digitales oficiales.

14. Mantener actualizado el repositorio del proyecto con la documentación en formatos .docx y .md, procurando que ambas versiones contengan la misma información y utilizando Git para conservar el historial de modificaciones realizadas durante el desarrollo.

15. Revisar al finalizar cada entregable que exista coherencia entre problema, objetivos, necesidades, requerimientos, arquitectura y pruebas, debido a que cualquier modificación realizada en una etapa puede requerir actualización de documentos anteriores para conservar la trazabilidad.

# BIBLIOGRAFÍA

Para el informe te recomiendo manejar esta sección con **formato APA 7**, utilizando principalmente normativa y documentos institucionales que sustentan el contexto legal y registral del proyecto.

Autoridad Nacional de Protección de Datos Personales. (2024). *Decreto Supremo N.° 016-2024-JUS: Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales*. Ministerio de Justicia y Derechos Humanos.

Congreso de la República del Perú. (2011). *Ley N.° 29733, Ley de Protección de Datos Personales*.

Superintendencia Nacional de los Registros Públicos. (2023). *Resolución de la Superintendencia Nacional de los Registros Públicos N.° 169-2023-SUNARP/SN*.

Superintendencia Nacional de los Registros Públicos. (2026). *Resolución Jefatural N.° 055-2026-SUNARP/ZRXII/JEF*.

Superintendencia Nacional de los Registros Públicos. (2026). *Resoluciones de la Jefatura Zonal – Zona Registral N.° XII – SUNARP*.

La Resolución Jefatural N.° 055-2026-SUNARP/ZRXII/JEF es especialmente útil para tu fundamentación porque declara procedente una anotación preventiva notarial por **presunta suplantación de identidad relacionada con una escritura pública**, por lo que sí constituye evidencia oficial directamente relacionada con el problema estudiado por NotaryVerify.

# WEBGRAFÍA

En la webgrafía puedes colocar principalmente la documentación técnica consultada para las tecnologías consideradas en el proyecto.

Google. (2026). *MediaPipe Face Landmarker*. Google AI for Developers.  
[<u>MediaPipe Face Landmarker</u>](https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/FaceLandmarker?utm_source=chatgpt.com)

OpenCV. (2026). *OpenCV Zoo: SFace Face Recognition Model*. OpenCV. El repositorio oficial describe SFace como un modelo de reconocimiento facial y proporciona ejemplos de utilización y evaluación.  
[<u>OpenCV Zoo – SFace</u>](https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface?utm_source=chatgpt.com)

OpenCV. (2026). *OpenCV Zoo*. OpenCV.  
[<u>OpenCV Zoo</u>](https://github.com/opencv/opencv_zoo?utm_source=chatgpt.com)

Autoridad Nacional de Protección de Datos Personales. (2024). *Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales*. Plataforma Digital Única del Estado Peruano.  
[<u>Reglamento de la Ley de Protección de Datos Personales</u>](https://www.gob.pe/institucion/anpd/normas-legales/6554453-16-2024-jus?utm_source=chatgpt.com)

Congreso de la República del Perú. (2011). *Ley N.° 29733 – Ley de Protección de Datos Personales*. Plataforma Digital Única del Estado Peruano.  
[<u>Ley N.° 29733</u>](https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/243470-29733?utm_source=chatgpt.com)

Superintendencia Nacional de los Registros Públicos. (2023). *Resolución N.° 169-2023-SUNARP/SN*. Plataforma Digital Única del Estado Peruano. La resolución dispone, desde el 2 de noviembre de 2023, la expedición con firma digital y presentación mediante SID-Sunarp de los partes y solicitudes notariales comprendidos por la disposición.  
[<u>Resolución N.° 169-2023-SUNARP/SN</u>](https://www.gob.pe/institucion/sunarp/normas-legales/4762089-169-2023-sunarp-sn?utm_source=chatgpt.com)

Superintendencia Nacional de los Registros Públicos. (2026). *Resolución Jefatural N.° 055-2026-SUNARP/ZRXII/JEF*. Plataforma Digital Única del Estado Peruano.  
[<u>Resolución Jefatural N.° 055-2026-SUNARP/ZRXII/JEF</u>](https://www.gob.pe/institucion/sunarp/normas-legales/8255003-055-2026-sunarp-zrxii-jef?utm_source=chatgpt.com)
