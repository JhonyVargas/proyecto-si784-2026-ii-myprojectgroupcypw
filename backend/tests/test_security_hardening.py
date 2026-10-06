"""CORS por entorno, validación de cargas y revisión estática (#22)."""

import re
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import app.core.seguridad as seguridad
import app.services.identidad_service as identidad_service_module
from app.core.database import get_db
from app.core.seguridad import ConfiguracionSeguridadError, resolver_max_upload, resolver_origenes_cors
from app.main import app
from app.models.db_models import DocumentoVerificado, IdentidadSimulada
from app.models.enums import RolUsuario
from app.services.auth_service import AuthService

BACKEND = Path(__file__).resolve().parent.parent
RAIZ = BACKEND.parent
JPEG = b"\xff\xd8\xff" + b"sintetico"
PNG = b"\x89PNG\r\n\x1a\n" + b"sintetico"


# ── Configuración ──

def test_origenes_por_defecto_son_la_estacion_local():
    assert resolver_origenes_cors({}) == ["http://127.0.0.1:5500", "http://localhost:5500"]


def test_origenes_explicitos_se_normalizan():
    assert resolver_origenes_cors({
        "NOTARYVERIFY_CORS_ORIGINS": " https://staging.example.test/ , http://127.0.0.1:5500",
    }) == ["https://staging.example.test", "http://127.0.0.1:5500"]


@pytest.mark.parametrize("valor", ["*", "https://ok.example.test,*", "staging.example.test", "ftp://x"])
def test_origenes_arbitrarios_o_invalidos_se_rechazan(valor):
    with pytest.raises(ConfiguracionSeguridadError):
        resolver_origenes_cors({"NOTARYVERIFY_CORS_ORIGINS": valor})


@pytest.mark.parametrize("valor", ["0", "-1", "cinco"])
def test_limite_de_carga_invalido_se_rechaza(valor):
    with pytest.raises(ConfiguracionSeguridadError):
        resolver_max_upload({"NOTARYVERIFY_MAX_UPLOAD_BYTES": valor})


def test_limite_de_carga_por_defecto():
    assert resolver_max_upload({}) == 5 * 1024 * 1024


# ── API ──

@pytest.fixture()
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        with TestClient(app) as cliente:
            yield cliente
    finally:
        app.dependency_overrides.clear()


def _token(client, db_session, rol, correo):
    AuthService(db_session).create_user("Usuario", correo, "clave", rol)
    token = client.post("/auth/login", json={"correo": correo, "password": "clave"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_cors_permite_estacion_local_y_rechaza_origen_arbitrario(client):
    preflight = {"Access-Control-Request-Method": "POST"}
    permitido = client.options("/auth/login", headers={"Origin": "http://127.0.0.1:5500", **preflight})
    ajeno = client.options("/auth/login", headers={"Origin": "https://atacante.example.test", **preflight})
    simple = client.get("/", headers={"Origin": "https://atacante.example.test"})

    assert permitido.status_code == 200
    assert permitido.headers["access-control-allow-origin"] == "http://127.0.0.1:5500"
    assert ajeno.status_code == 400
    assert "access-control-allow-origin" not in ajeno.headers
    assert "access-control-allow-origin" not in simple.headers


def _registrar(client, headers, archivo):
    return client.post("/identidades", headers=headers, data={
        "nombre_ficticio": "PERSONA-CARGA", "documento_ficticio": "CARGA-001",
        "id_participante": "voluntario-carga", "confirmo_dato_ficticio": "true",
    }, files={"imagen_referencia": archivo})


@pytest.mark.parametrize("archivo,status,code", [
    (("ref.gif", b"GIF89a-sintetico", "image/gif"), 415, "UPLOAD_TYPE_NOT_ALLOWED"),
    (("ref.jpg", b"texto que dice ser jpeg", "image/jpeg"), 415, "UPLOAD_TYPE_NOT_ALLOWED"),
    (("ref.png", JPEG, "image/png"), 415, "UPLOAD_TYPE_NOT_ALLOWED"),
    (("ref.jpg", b"", "image/jpeg"), 422, "UPLOAD_EMPTY"),
])
def test_carga_invalida_se_rechaza_sin_persistir(client, db_session, tmp_path, monkeypatch, archivo, status, code):
    monkeypatch.setattr(identidad_service_module, "REFERENCIAS_DIR", tmp_path)
    admin = _token(client, db_session, RolUsuario.ADMINISTRADOR, "admin.carga@example.test")

    respuesta = _registrar(client, admin, archivo)

    assert respuesta.status_code == status
    assert respuesta.json()["detail"]["code"] == code
    assert db_session.query(IdentidadSimulada).count() == 0
    assert list(tmp_path.iterdir()) == []


def test_carga_que_supera_el_limite_se_rechaza(client, db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(identidad_service_module, "REFERENCIAS_DIR", tmp_path)
    monkeypatch.setattr(seguridad, "MAX_UPLOAD_BYTES", 16)
    admin = _token(client, db_session, RolUsuario.ADMINISTRADOR, "admin.limite@example.test")

    respuesta = _registrar(client, admin, ("ref.png", PNG + b"x" * 64, "image/png"))

    assert respuesta.status_code == 413
    assert respuesta.json()["detail"]["code"] == "UPLOAD_TOO_LARGE"
    assert list(tmp_path.iterdir()) == []


def test_carga_sin_credenciales_se_rechaza(client):
    respuesta = client.post(
        "/verificaciones/cualquiera/rostro", files={"imagen": ("r.jpg", JPEG, "image/jpeg")}
    )
    assert respuesta.status_code == 401


def test_documento_requiere_credenciales_sesion_existente_y_cuerpo(client, db_session):
    sin_token = client.post("/documentos", params={"id_sesion": "x"}, data={"contenido": "c"})
    operador = _token(client, db_session, RolUsuario.OPERADOR, "operador.doc@example.test")
    inexistente = client.post(
        "/documentos", headers=operador, params={"id_sesion": "no-existe"}, data={"contenido": "c"}
    )
    en_url = client.post("/documentos", headers=operador, params={"id_sesion": "x", "contenido": "c"})

    assert sin_token.status_code == 401
    assert inexistente.status_code == 404
    assert inexistente.json()["detail"]["code"] == "SESSION_NOT_FOUND"
    assert en_url.status_code == 422
    assert db_session.query(DocumentoVerificado).count() == 0


# ── Revisión estática ──

_SENSIBLE = re.compile(r"token|password|contrase|imagen|contenido|hash", re.IGNORECASE)


def test_codigo_no_registra_datos_sensibles_en_logs():
    """Ningún print/log del backend recibe tokens, contraseñas, imágenes ni documentos."""
    hallazgos = []
    for archivo in (BACKEND / "app").rglob("*.py"):
        for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"\b(print|logger\.\w+|logging\.\w+)\(", linea) and _SENSIBLE.search(linea):
                hallazgos.append(f"{archivo.relative_to(BACKEND)}:{numero}")
    assert hallazgos == []


_SECRETO = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"
    r"|(?:PASSWORD|SECRET|TOKEN)\s*=\s*['\"]?[A-Za-z0-9!@#$%^&*_\-]{8,}",
)


def test_repositorio_no_versiona_secretos():
    archivos = subprocess.run(
        ["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    hallazgos = []
    for relativo in archivos:
        ruta = RAIZ / relativo
        if ruta.suffix in {".png", ".jpg", ".jpeg", ".ico", ".pdf", ".docx"} or not ruta.is_file():
            continue
        texto = ruta.read_text(encoding="utf-8", errors="ignore")
        for coincidencia in _SECRETO.finditer(texto):
            linea = texto[: coincidencia.start()].count("\n") + 1
            if "use-una-clave" not in texto.splitlines()[linea - 1]:
                hallazgos.append(f"{relativo}:{linea}")
    assert hallazgos == []
