# NotaryVerify — Frontend

Cliente estático de la estación de verificación y panel administrativo. La
entrada canónica es `index.html`; consume la API local en
`http://127.0.0.1:8000` y ofrece verificación, administración de identidades y
credenciales, y auditoría.

## Ejecutar

Inicia el backend antes. Después, desde esta carpeta:

```powershell
python -m http.server 5500
```

Abre `http://127.0.0.1:5500`. La aplicación requiere permiso de cámara solo
para los flujos que capturan imágenes. `legacy-baseline/` conserva el panel
anterior y `app/` conserva la fuente comparada hasta que el equipo complete la
validación manual y decida su retiro.

No incluyas fotos de clientes, datos reales ni credenciales institucionales en
el navegador ni en archivos del repositorio.
