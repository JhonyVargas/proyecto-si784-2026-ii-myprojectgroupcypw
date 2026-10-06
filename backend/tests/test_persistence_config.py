"""Configuración de persistencia por entorno y cambios de esquema (#21)."""

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect

from app.core.database import (
    DATA_DIR_POR_DEFECTO,
    ConfiguracionPersistenciaError,
    EsquemaIncompatibleError,
    resolver_configuracion,
    verificar_esquema,
)
from app.core.reset_db import reiniciar_base

BACKEND = Path(__file__).resolve().parent.parent


def test_configuracion_por_defecto_conserva_rutas_del_prototipo():
    data_dir, url = resolver_configuracion({})

    assert data_dir == DATA_DIR_POR_DEFECTO.resolve()
    assert data_dir == (BACKEND / "data").resolve()
    assert url == f"sqlite:///{(DATA_DIR_POR_DEFECTO / 'notaryverify.db').as_posix()}"


def test_variables_vacias_equivalen_a_no_definirlas():
    assert resolver_configuracion({
        "NOTARYVERIFY_DATA_DIR": "", "NOTARYVERIFY_DATABASE_URL": "",
    }) == resolver_configuracion({})


def test_configuracion_explicita(tmp_path):
    url = f"sqlite:///{(tmp_path / 'otra.db').as_posix()}"
    data_dir, resuelta = resolver_configuracion({
        "NOTARYVERIFY_DATA_DIR": str(tmp_path), "NOTARYVERIFY_DATABASE_URL": url,
    })

    assert data_dir == tmp_path.resolve()
    assert resuelta == url


def test_data_dir_explicito_deriva_la_base(tmp_path):
    _, url = resolver_configuracion({"NOTARYVERIFY_DATA_DIR": str(tmp_path)})

    assert url == f"sqlite:///{(tmp_path / 'notaryverify.db').as_posix()}"


@pytest.mark.parametrize("url", [
    "postgresql://usuario@localhost/notaryverify", "mysql://localhost/db", "notaryverify.db",
])
def test_url_no_sqlite_se_rechaza(url):
    with pytest.raises(ConfiguracionPersistenciaError, match="solo admite SQLite"):
        resolver_configuracion({"NOTARYVERIFY_DATABASE_URL": url})


def _sql(ruta, *sentencias):
    """Ejecuta y cierra la conexión: en Windows un archivo abierto no puede reemplazarse."""
    conexion = sqlite3.connect(ruta)
    try:
        filas = [conexion.execute(s).fetchall() for s in sentencias]
        conexion.commit()
        return filas
    finally:
        conexion.close()


def _motor(ruta):
    return create_engine(f"sqlite:///{ruta.as_posix()}")


def test_esquema_vacio_se_crea_completo(tmp_path):
    motor = _motor(tmp_path / "nueva.db")
    verificar_esquema(motor)

    assert {"usuarios", "sesiones_verificacion", "evidencias_tramite"} <= set(inspect(motor).get_table_names())
    motor.dispose()


def test_tabla_aditiva_faltante_se_crea_sin_tocar_datos(tmp_path):
    ruta = tmp_path / "aditiva.db"
    motor = _motor(ruta)
    verificar_esquema(motor)
    motor.dispose()
    _sql(ruta, "DROP TABLE evidencias_tramite")

    motor = _motor(ruta)
    verificar_esquema(motor)

    assert "evidencias_tramite" in inspect(motor).get_table_names()
    motor.dispose()


def test_columna_faltante_detiene_arranque_con_instrucciones(tmp_path):
    ruta = tmp_path / "antigua.db"
    _sql(ruta, "CREATE TABLE usuarios (id VARCHAR PRIMARY KEY)")

    motor = _motor(ruta)
    with pytest.raises(EsquemaIncompatibleError) as error:
        verificar_esquema(motor)
    motor.dispose()

    assert "usuarios.correo" in str(error.value)
    assert "python -m app.core.reset_db" in str(error.value)


def test_reinicio_respalda_y_recrea_base_incompatible(tmp_path):
    ruta = tmp_path / "notaryverify.db"
    _sql(ruta, "CREATE TABLE usuarios (id VARCHAR PRIMARY KEY)", "INSERT INTO usuarios VALUES ('sintetico')")
    url = f"sqlite:///{ruta.as_posix()}"

    respaldo = reiniciar_base(url, tmp_path)

    assert respaldo is not None and respaldo.parent == tmp_path / "respaldo"
    assert _sql(respaldo, "SELECT id FROM usuarios") == [[("sintetico",)]]
    motor = _motor(ruta)
    verificar_esquema(motor)
    assert "correo" in {c["name"] for c in inspect(motor).get_columns("usuarios")}
    motor.dispose()


def test_reinicio_no_aplica_a_memoria(tmp_path):
    with pytest.raises(ValueError):
        reiniciar_base("sqlite:///:memory:", tmp_path)


def test_arranque_real_con_configuracion_explicita(tmp_path):
    """Importa la app e inicia la base en un proceso aparte con entorno explícito."""
    entorno = {
        **os.environ,
        "NOTARYVERIFY_DATA_DIR": str(tmp_path),
        "NOTARYVERIFY_DATABASE_URL": "",
    }
    for clave in [c for c in entorno if c.startswith("NOTARYVERIFY_BOOTSTRAP_")]:
        entorno.pop(clave)
    codigo = "from app.core.database import DATABASE_URL, init_db; init_db(); print(DATABASE_URL)"

    salida = subprocess.run(
        [sys.executable, "-c", codigo], cwd=BACKEND, env=entorno,
        capture_output=True, text=True, timeout=120,
    )

    assert salida.returncode == 0, salida.stderr
    assert (tmp_path / "notaryverify.db").exists()
    assert salida.stdout.strip().endswith(f"{tmp_path.resolve().as_posix()}/notaryverify.db")


def test_arranque_real_rechaza_url_invalida(tmp_path):
    entorno = {**os.environ, "NOTARYVERIFY_DATABASE_URL": "postgresql://localhost/x"}

    salida = subprocess.run(
        [sys.executable, "-c", "import app.core.database"], cwd=BACKEND, env=entorno,
        capture_output=True, text=True, timeout=120,
    )

    assert salida.returncode != 0
    assert "solo admite SQLite" in salida.stderr
