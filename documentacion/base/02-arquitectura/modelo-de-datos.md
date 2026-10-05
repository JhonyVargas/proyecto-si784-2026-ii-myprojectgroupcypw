# Modelo de datos

La base actual es SQLite local en backend/data/notaryverify.db y se crea con Base.metadata.create_all al iniciar.

| Grupo | Tablas / finalidad |
| --- | --- |
| Consentimiento e identidad | consentimientos_biometricos, identidades_simuladas, solicitudes_cambio_referencia |
| Credenciales y usuario | credenciales, usuarios, sesiones_usuario |
| Verificación | sesiones_verificacion, desafios_prueba_vida, configuraciones_reglas, decisiones_reglas |
| Evidencia | eventos_auditoria, documentos_verificados, tramites_simulados |

Los datos, modelos descargados y cargas son runtime ignorado. No se deben versionar fotos biométricas ni bases SQLite. Un cambio de esquema debe describir compatibilidad, estrategia de reinicio o migración y pruebas antes de implementarse.

`sesiones_usuario` es una tabla aditiva de autenticación local: almacena el
hash SHA-256 del token opaco, vencimiento y revocación, nunca el token ni la
contraseña en texto plano. Es compatible con las bases SQLite existentes porque
no modifica tablas previas; `create_all` crea solo esa tabla. El reinicio de la
base local es exclusivamente una opción para datos sintéticos de desarrollo.

Las sesiones de verificación persisten `id_responsable`, credencial, identidad,
factores, resultado, estado e inicio/fin. La vigencia de diez minutos se
materializa al consultar u operar; no requiere un worker y no altera el esquema
SQLite existente.

`alertas_intentos_fallidos` es una tabla aditiva que registra identidad,
contador, inicio, vencimiento y resolución del bloqueo temporal RN-05. Es
compatible con SQLite local existente; no modifica tablas preexistentes ni
guarda biometría.

`solicitudes_cambio_referencia` es una tabla aditiva para RN-09: conserva actor,
motivo, fechas, decisión y una ruta runtime temporal. La referencia pendiente
vive solo en `backend/data/referencias_pendientes`; al aprobarse se reemplaza
atómicamente la referencia activa y se elimina la anterior, y al rechazarse se
elimina la pendiente. La bitácora no incluye la ruta ni contenido de imágenes.
Las bases SQLite existentes son compatibles porque no se modifica una tabla
previa; el reinicio local sigue aplicando solo a datos sintéticos.

`desafios_prueba_vida` será una tabla aditiva para RF-06. Guardará únicamente
la sesión, acción aleatoria, emisión, vencimiento, estado y número de reintentos
del desafío; no almacena vídeo, imágenes, landmarks ni métricas biométricas.
El despliegue local debe respaldar o reiniciar `backend/data/notaryverify.db`
antes de actualizar hasta que exista una migración formal: `create_all` crea la
tabla nueva pero no es un gestor de migraciones. Las pruebas usarán SQLite en
memoria y verificarán emisión, vencimiento, repetición y rechazo controlado.

`configuraciones_reglas` y `decisiones_reglas` son tablas aditivas para RF-16.
La primera conserva una versión y prioridades validadas; la segunda vincula una
sesión con la versión y una instantánea JSON de la configuración aplicada, sin
biometría. No se modifica `sesiones_verificacion`: las bases SQLite existentes
deben respaldarse o reiniciarse con datos sintéticos antes de actualizar hasta
contar con migraciones formales; `create_all` crea solo las tablas nuevas.
