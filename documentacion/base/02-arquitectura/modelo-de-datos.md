# Modelo de datos

La base actual es SQLite local en backend/data/notaryverify.db y se crea con Base.metadata.create_all al iniciar.

| Grupo | Tablas / finalidad |
| --- | --- |
| Consentimiento e identidad | consentimientos_biometricos, identidades_simuladas |
| Credenciales y usuario | credenciales, usuarios |
| Verificación | sesiones_verificacion |
| Evidencia | eventos_auditoria, documentos_verificados, tramites_simulados |

Los datos, modelos descargados y cargas son runtime ignorado. No se deben versionar fotos biométricas ni bases SQLite. Un cambio de esquema debe describir compatibilidad, estrategia de reinicio o migración y pruebas antes de implementarse.
