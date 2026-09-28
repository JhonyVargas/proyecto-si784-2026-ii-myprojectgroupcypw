# Decisiones técnicas

| Decisión | Motivo | Alternativa descartada |
| --- | --- | --- |
| FastAPI + Pydantic | Ya implementado y probado | Reescritura con NestJS |
| SQLAlchemy + SQLite | Adecuado para prototipo local sintético | Servidor de base de datos innecesario |
| HTML, CSS y JavaScript | Panel de cámara sin build | Migración a framework sin valor para MVP |
| OpenCV y MediaPipe locales | Evita biometría comercial | API biométrica externa |
| Docker Compose local | Reproduce entorno | Plataforma cloud |

Pendiente: configuración DATABASE_URL, CORS restrictivo y migraciones formales se tratarán en una propuesta posterior porque afectan compatibilidad.
