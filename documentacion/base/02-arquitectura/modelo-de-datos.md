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
