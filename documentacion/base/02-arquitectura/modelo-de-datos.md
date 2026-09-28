# Modelo de datos

La base actual es SQLite local en backend/data/notaryverify.db y se crea con Base.metadata.create_all al iniciar.

| Grupo | Tablas / finalidad |
| --- | --- |
| Consentimiento e identidad | consentimientos_biometricos, identidades_simuladas |
| Credenciales y usuario | credenciales, usuarios, sesiones_usuario |
| Verificación | sesiones_verificacion |
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
