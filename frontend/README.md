# NotaryVerify — Frontend (panel de pruebas)

Interfaz web mínima en HTML + CSS + JavaScript plano (sin build ni
dependencias) que consume la API del backend para ejecutar el flujo
completo de verificación multicapa (CU-03 del `FD03`).

## Cómo usarlo

1. Inicia primero el backend (ver `../backend/README.md`), por defecto en
   `http://127.0.0.1:8000`.
2. Abre `index.html` directamente en el navegador, o sirve la carpeta con
   cualquier servidor estático, por ejemplo:

   ```bash
   cd frontend
   python -m http.server 5500
   ```

   y visita `http://127.0.0.1:5500`.
3. Si el backend corre en otra dirección/puerto, ajústalo en el campo
   "API" de la cabecera de la página.

## Flujo de la interfaz

1. **Simulador de Identidad**: otorgar consentimiento del participante y
   registrar una identidad ficticia con una fotografía de referencia.
2. **Credencial**: emitir una credencial QR para la identidad registrada
   (y opcionalmente revocarla, para probar RN-04).
3. **Verificación multicapa**: iniciar sesión con el código de la
   credencial, enviar una foto de rostro y luego una foto para la prueba
   de vida (parpadeo o giro), obteniendo el resultado final.
4. **Bitácora de auditoría**: verificar la integridad de la cadena de
   hashes y listar todos los eventos registrados.
