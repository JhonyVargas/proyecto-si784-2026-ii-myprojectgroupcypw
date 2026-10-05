# Diseño: comparación facial reproducible

La comparación conserva OpenCV y LBPH. Antes de comparar exige una imagen de
al menos 120 × 120 píxeles, exactamente un rostro y una varianza de Laplaciano
de al menos 20 en el recorte. La distancia LBPH se normaliza a `[0, 1]` con
`max(0, 1 - distancia/100)` y se acepta desde 0.35.

Los rechazos se modelan como errores de dominio y la API los traduce a códigos
422 estables. Las pruebas reemplazan imágenes y detectores reales por patrones
sintéticos y dobles de prueba; así no guardan biometría ni requieren red.
