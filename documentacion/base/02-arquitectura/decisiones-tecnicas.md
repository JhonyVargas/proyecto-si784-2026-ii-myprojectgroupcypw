# Decisiones técnicas

| Decisión | Motivo | Alternativa descartada |
| --- | --- | --- |
| FastAPI + Pydantic | Ya implementado y probado | Reescritura con NestJS |
| SQLAlchemy + SQLite | Adecuado para prototipo local sintético | Servidor de base de datos innecesario |
| HTML, CSS y JavaScript | Panel de cámara sin build | Migración a framework sin valor para MVP |
| OpenCV y MediaPipe locales | Evita biometría comercial | API biométrica externa |
| Docker Compose local | Reproduce entorno | Plataforma cloud |
| RFID simulado con UID hexadecimal | No hay hardware disponible; permite probar contrato de lectura sin inventar integración física | Lector RFID físico sin evidencia de disponibilidad |
| Umbral facial local 0.35 y calidad mínima | Hace reproducible el resultado técnico de LBPH sin afirmar precisión biométrica; exige 120 × 120 px, un rostro y nitidez mínima | Elegir el rostro más grande o aceptar capturas ambiguas |

Pendiente: configuración DATABASE_URL, CORS restrictivo y migraciones formales se tratarán en una propuesta posterior porque afectan compatibilidad.

La decisión RFID vigente es: no se dispone de lector físico en esta etapa. El
adaptador local acepta UID hexadecimales en mayúsculas y sin separadores (por
ejemplo, `04A1B2C3`). Una futura integración física deberá implementar el
puerto `LectorRfid` sin cambiar reglas, credenciales ni la API de verificación.

El clasificador Haar y el modelo de MediaPipe se conservan como artefactos de
ejecución local (`backend/data/modelos`) y pueden requerir una descarga inicial
para una demostración real. Esto no afecta a la suite automatizada: sus pruebas
biométricas usan fixtures sintéticas y adaptadores simulados sin red, cámara ni
biometría de personas.
