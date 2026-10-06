"""Recorrido de compatibilidad en Chrome, Edge y Firefox (#25, RNF-08).

Requisitos: backend en http://127.0.0.1:8000 y frontend en http://127.0.0.1:5500
(ver README), `pip install -r frontend/e2e/requirements.txt` y
`python -m playwright install firefox`. Chrome y Edge se usan instalados.

Variables: NOTARYVERIFY_E2E_ADMIN_EMAIL/PASSWORD y
NOTARYVERIFY_E2E_OPERATOR_EMAIL/PASSWORD (cuentas sintéticas locales).

    python frontend/e2e/recorrido_navegadores.py --salida resultados.json

Escenarios por navegador, con cámara simulada por el navegador (sin personas):
1. flujo_camara: API conectada, login de Operador, credencial válida, vídeo en
   vivo y captura; el fotograma sintético no tiene rostro y la estación debe
   mostrar el motivo de forma recuperable.
2. camara_denegada: getUserMedia rechaza con NotAllowedError y la estación
   explica cómo autorizar la cámara y ofrece subir una fotografía.
3. api_caida: las llamadas a la API fallan y la estación lo indica.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import expect, sync_playwright

API = "http://127.0.0.1:8000"
WEB = "http://127.0.0.1:5500"
ESPERA_MS = 15_000

DENEGAR_CAMARA = """
navigator.mediaDevices.getUserMedia = () =>
  Promise.reject(new DOMException("Permiso denegado", "NotAllowedError"));
"""


def _api(ruta: str, token: str | None = None, json_body=None, data=None, headers=None):
    cabeceras = dict(headers or {})
    if token:
        cabeceras["Authorization"] = f"Bearer {token}"
    cuerpo = None
    if json_body is not None:
        cuerpo = json.dumps(json_body).encode()
        cabeceras["Content-Type"] = "application/json"
    elif data is not None:
        cuerpo = data
    solicitud = urllib.request.Request(API + ruta, data=cuerpo, headers=cabeceras, method="POST")
    with urllib.request.urlopen(solicitud, timeout=30) as respuesta:
        return json.loads(respuesta.read())


def _multipart(campos: dict, archivo: tuple[str, str, bytes, str]):
    limite = "----notaryverify-e2e"
    partes = []
    for nombre, valor in campos.items():
        partes.append(f'--{limite}\r\nContent-Disposition: form-data; name="{nombre}"\r\n\r\n{valor}\r\n'.encode())
    nombre, archivo_nombre, contenido, tipo = archivo
    partes.append(
        f'--{limite}\r\nContent-Disposition: form-data; name="{nombre}"; filename="{archivo_nombre}"\r\n'
        f"Content-Type: {tipo}\r\n\r\n".encode() + contenido + b"\r\n"
    )
    partes.append(f"--{limite}--\r\n".encode())
    return b"".join(partes), {"Content-Type": f"multipart/form-data; boundary={limite}"}


def preparar_credencial() -> str:
    """Identidad y credencial ficticias para el recorrido; imagen sintética sin rostro."""
    token = _api("/auth/login", json_body={
        "correo": os.environ["NOTARYVERIFY_E2E_ADMIN_EMAIL"],
        "password": os.environ["NOTARYVERIFY_E2E_ADMIN_PASSWORD"],
    })["access_token"]
    sufijo = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    participante = f"e2e-{sufijo}"
    _api("/identidades/consentimientos", token, json_body={"id_participante": participante})
    imagen = cv2.imencode(".jpg", np.full((240, 240, 3), 128, dtype=np.uint8))[1].tobytes()
    cuerpo, cabeceras = _multipart({
        "nombre_ficticio": f"PERSONA-E2E-{sufijo}", "documento_ficticio": f"E2E-{sufijo}",
        "id_participante": participante, "confirmo_dato_ficticio": "true",
    }, ("imagen_referencia", "referencia.jpg", imagen, "image/jpeg"))
    identidad = _api("/identidades", token, data=cuerpo, headers=cabeceras)
    return _api("/credenciales", token, json_body={"id_identidad": identidad["id"]})["codigo"]


def _login(pagina):
    pagina.fill("#login-correo", os.environ["NOTARYVERIFY_E2E_OPERATOR_EMAIL"])
    pagina.fill("#login-password", os.environ["NOTARYVERIFY_E2E_OPERATOR_PASSWORD"])
    pagina.click("#form-login button[type=submit]")
    expect(pagina.locator("#sesion-activa")).to_be_visible(timeout=ESPERA_MS)


def _iniciar(pagina, codigo: str):
    pagina.fill("#entrada-codigo", codigo)
    pagina.click("#boton-iniciar")
    expect(pagina.locator("#pantalla-rostro")).to_have_class("pantalla pantalla--activa", timeout=ESPERA_MS)


def escenario_flujo_camara(pagina, codigo: str) -> str:
    pagina.goto(WEB)
    expect(pagina.locator("#texto-api")).to_contain_text("API conectada", timeout=ESPERA_MS)
    _login(pagina)
    _iniciar(pagina, codigo)
    pagina.wait_for_function(
        "() => document.querySelector('#video-rostro').videoWidth > 0", timeout=ESPERA_MS
    )
    pagina.click("#boton-capturar-rostro")
    error = pagina.locator("#error-rostro")
    expect(error).to_be_visible(timeout=ESPERA_MS)
    return f"vídeo en vivo; captura sin rostro informada: {error.inner_text().strip()}"


def escenario_camara_denegada(pagina, codigo: str) -> str:
    pagina.add_init_script(DENEGAR_CAMARA)
    pagina.goto(WEB)
    _login(pagina)
    _iniciar(pagina, codigo)
    motivo = pagina.locator("#motivo-camara-rostro")
    expect(pagina.locator("#sin-camara-rostro")).to_be_visible(timeout=ESPERA_MS)
    expect(motivo).to_contain_text("Se denegó el permiso de cámara")
    return f"alternativa de subir fotografía visible: {motivo.inner_text().strip()}"


def escenario_api_caida(pagina, _codigo: str) -> str:
    pagina.route(f"{API}/**", lambda ruta: ruta.abort())
    pagina.goto(WEB)
    expect(pagina.locator("#texto-api")).to_have_text("API no disponible", timeout=ESPERA_MS)
    pagina.fill("#login-correo", "operador@example.test")
    pagina.fill("#login-password", "clave-cualquiera")
    pagina.click("#form-login button[type=submit]")
    error = pagina.locator("#error-login")
    expect(error).to_be_visible(timeout=ESPERA_MS)
    return f"indicador y mensaje: {error.inner_text().strip()}"


ESCENARIOS = {
    "flujo_camara": escenario_flujo_camara,
    "camara_denegada": escenario_camara_denegada,
    "api_caida": escenario_api_caida,
}


def _navegadores(p):
    chromium_args = ["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"]
    yield "Chrome", lambda: p.chromium.launch(channel="chrome", args=chromium_args)
    yield "Edge", lambda: p.chromium.launch(channel="msedge", args=chromium_args)
    yield "Firefox", lambda: p.firefox.launch(firefox_user_prefs={
        "media.navigator.streams.fake": True,
        "media.navigator.permission.disabled": True,
    })


def ejecutar() -> list[dict]:
    codigo = preparar_credencial()
    resultados = []
    with sync_playwright() as p:
        for nombre, lanzar in _navegadores(p):
            navegador = lanzar()
            version = navegador.version
            for escenario, funcion in ESCENARIOS.items():
                contexto = navegador.new_context()
                pagina = contexto.new_page()
                try:
                    detalle, aprobado = funcion(pagina, codigo), True
                except (AssertionError, PlaywrightError) as error:
                    detalle, aprobado = str(error).splitlines()[0], False
                finally:
                    contexto.close()
                resultados.append({
                    "navegador": nombre, "version": version, "escenario": escenario,
                    "aprobado": aprobado, "detalle": detalle,
                })
            navegador.close()
    return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--salida", type=Path)
    args = parser.parse_args()
    resultados = ejecutar()
    texto = json.dumps({
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "resultados": resultados,
    }, ensure_ascii=False, indent=2)
    if args.salida:
        args.salida.write_text(texto + "\n", encoding="utf-8")
    print(texto)
    return 0 if all(r["aprobado"] for r in resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
