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
| Persistencia configurable por entorno y reinicio verificado (#21) | `NOTARYVERIFY_DATA_DIR` y `NOTARYVERIFY_DATABASE_URL` con valores por defecto idénticos al prototipo; al iniciar se crean tablas aditivas y se rechaza un esquema con columnas faltantes, con respaldo y reinicio reproducible | Alembic: añade dependencia y migraciones para datos solo sintéticos; motor de base de datos servidor |
| Desafío de vida en servidor | Evita que el cliente elija la acción; registra emisión, vencimiento y una repetición sin conservar vídeo | Confiar en un sorteo JavaScript o almacenar capturas biométricas |

CORS por entorno, validación de cargas y la guía HTTPS se decidieron en #22 (ver `../04-calidad-operacion/seguridad.md`). La configuración de persistencia y la estrategia de cambios de esquema quedaron decididas en #21 (ver `modelo-de-datos.md`, sección "Configuración y cambios de esquema").

La decisión RFID vigente es: no se dispone de lector físico en esta etapa. El
adaptador local acepta UID hexadecimales en mayúsculas y sin separadores (por
ejemplo, `04A1B2C3`). Una futura integración física deberá implementar el
puerto `LectorRfid` sin cambiar reglas, credenciales ni la API de verificación.

El clasificador Haar y el modelo de MediaPipe se conservan como artefactos de
ejecución local (`backend/data/modelos`) y pueden requerir una descarga inicial
para una demostración real. Esto no afecta a la suite automatizada: sus pruebas
biométricas usan fixtures sintéticas y adaptadores simulados sin red, cámara ni
biometría de personas.

La prueba de vida es experimental. MediaPipe observa una acción en una única
captura posterior a un desafío breve; controla ausencia/multiplicidad de rostro,
timeout y acciones no detectadas. Las pruebas de fotografía impresa y en
pantalla son escenarios sintéticos de acción estática no cumplida: no se afirma
que el sistema pueda distinguir el soporte físico de cualquier píxel recibido.
