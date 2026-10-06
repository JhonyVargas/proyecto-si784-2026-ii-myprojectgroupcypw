# Rendimiento: protocolo y resultados (#24)

Mediciones de RNF-02 (comparación facial promedio menor de 3 s) y RNF-04 (flujo
completo menor de 45 s). Se separan dos niveles, como pide la issue:

| Nivel | Qué mide | Quién lo ejecuta | Estado |
| --- | --- | --- | --- |
| Benchmark técnico | costo de cómputo del sistema, sin personas | automatizado | ejecutado 2026-10-05 |
| Medición con cámara | flujo real con operador y voluntario consentido | equipo | pendiente de ejecución |

## 1. Benchmark técnico automatizado

### Protocolo

Desde `backend`:

```
python -m benchmarks.medir_rendimiento --comparaciones 20 --sesiones 20 --salida reporte.json
```

- **Muestras:** JPEG sintéticos de 640 × 480 generados con ruido de semilla
  fija; no contienen rostros ni datos de personas y no se versionan.
- **Comparación facial (20 ejecuciones):** `BiometriaService.comparar_rostro`
  completo: decodificación, detector Haar real, filtro de nitidez, recorte,
  normalización, ecualización y LBPH (entrenamiento y predicción).
- **Flujo del sistema (20 sesiones):** por HTTP y con SQLite en memoria: login,
  inicio con credencial, captura facial, desafío y prueba de vida con MediaPipe
  Face Landmarker real. Cada sesión debe terminar en `IDENTIDAD_VERIFICADA`.
- **Inyección declarada:** como las imágenes no tienen rostros, la posición del
  rostro y el resultado de la acción de vida se inyectan *después* de ejecutar
  el detector real. Se mide el costo de los modelos, no su precisión.
- **Modelos:** se usan solo si ya existen en `<DATA_DIR>/modelos`; el benchmark
  nunca los descarga. El reporte indica si fueron reales.
- **Calentamiento:** una comparación previa descartada para excluir la carga
  perezosa de modelos.
- **Métricas:** promedio, mediana, p95, mínimo y máximo en segundos.
- **Criterio de aceptación:** promedio menor que el umbral (3 s y 45 s). El
  comando termina con código 1 si alguno no se cumple.

### Resultados del 2026-10-05

Entorno: Windows 11, AMD64 Family 25 (16 núcleos lógicos), Python 3.14.4,
OpenCV 5.0.0, MediaPipe 1.0.1, FastAPI 0.141.1; detector Haar y Face Landmarker
reales.

| Medición | n | Promedio | Mediana | p95 | Máx. | Umbral | Cumple |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Comparación facial | 20 | 0,0209 s | 0,0204 s | 0,0245 s | 0,0261 s | 3 s | Sí |
| Flujo del sistema | 20 | 0,1021 s | 0,0962 s | 0,1149 s | 0,1763 s | 45 s | Sí |

### Regresión controlada

`backend/tests/test_rendimiento.py` ejecuta el mismo benchmark con 5
comparaciones y 3 sesiones en cada `pytest`, también en CI, donde no hay
modelos descargados y se mide el resto del pipeline. Falla si un promedio supera
su umbral.

### Limitaciones

- El costo de detección depende de la resolución y del hardware; una cámara de
  mayor resolución o un equipo más lento pueden aumentar los tiempos.
- No incluye latencia de red, cámara del navegador ni tiempo humano.
- No mide precisión, FPR ni resistencia a suplantación (#26 y #27).

## 2. Medición con cámara (pendiente del equipo)

1. Iniciar backend y frontend según la [guía local](despliegue.md) en el equipo
   de demostración y registrar su hardware.
2. Con una identidad ficticia de un voluntario con consentimiento, ejecutar 20
   verificaciones completas desde "Iniciar verificación" hasta el resultado.
3. Tomar la duración de cada sesión como `fecha_fin - fecha_inicio` del
   historial administrativo (`GET /verificaciones`), sin capturar imágenes.
4. Registrar aquí promedio, mediana, p95 y desviaciones, sin datos personales.

## Desviaciones y decisiones

- 2026-10-05: ninguna medición superó su umbral; no se abre issue de
  optimización. Decisión: el cumplimiento de RNF-04 con tiempo humano queda
  sujeto a la medición con cámara de la sección 2; hasta entonces solo se afirma
  el costo técnico del sistema.
- Si una medición futura supera un umbral, se registra aquí con su entorno y se
  abre una issue antes de cambiar algoritmos.
