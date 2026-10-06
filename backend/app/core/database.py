"""Configuración de la base de datos SQLite del prototipo NotaryVerify.

La ubicación se obtiene del entorno (#21):

- NOTARYVERIFY_DATA_DIR: carpeta runtime (por defecto backend/data).
- NOTARYVERIFY_DATABASE_URL: URL SQLAlchemy; solo se admite SQLite
  (por defecto sqlite:///<DATA_DIR>/notaryverify.db).

Una variable vacía equivale a no definirla. Ver
documentacion/base/02-arquitectura/modelo-de-datos.md.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATA_DIR_POR_DEFECTO = Path(__file__).resolve().parent.parent.parent / "data"


class ConfiguracionPersistenciaError(RuntimeError):
    """La configuración de persistencia del entorno no es válida."""


class EsquemaIncompatibleError(RuntimeError):
    """La base existente no tiene columnas que los modelos requieren."""


def resolver_configuracion(entorno: Mapping[str, str] = os.environ) -> tuple[Path, str]:
    """Devuelve (DATA_DIR, DATABASE_URL) a partir del entorno, validados."""
    data_dir = Path(entorno.get("NOTARYVERIFY_DATA_DIR") or DATA_DIR_POR_DEFECTO).expanduser()
    url = entorno.get("NOTARYVERIFY_DATABASE_URL") or (
        f"sqlite:///{(data_dir / 'notaryverify.db').as_posix()}"
    )
    if not url.startswith("sqlite://"):
        raise ConfiguracionPersistenciaError(
            "NOTARYVERIFY_DATABASE_URL solo admite SQLite (sqlite:///ruta.db); "
            "un motor de base de datos servidor está fuera del alcance del prototipo."
        )
    return data_dir.resolve(), url


def ruta_sqlite(url: str) -> Path | None:
    """Ruta del archivo SQLite de la URL, o None si la base es en memoria."""
    ruta = url.removeprefix("sqlite:///") if url.startswith("sqlite:///") else ""
    if not ruta or ruta == ":memory:":
        return None
    return Path(ruta)


DATA_DIR, DATABASE_URL = resolver_configuracion()
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if (ruta := ruta_sqlite(DATABASE_URL)) is not None:
        ruta.parent.mkdir(parents=True, exist_ok=True)
except OSError as exc:
    raise ConfiguracionPersistenciaError(
        f"No se puede crear la carpeta de datos configurada: {exc}"
    ) from exc

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verificar_esquema(motor: Engine) -> None:
    """Crea tablas aditivas y rechaza tablas existentes con columnas faltantes."""
    from app.models import db_models  # noqa: F401 (registra las tablas en Base.metadata)

    Base.metadata.create_all(bind=motor)
    inspector = inspect(motor)
    faltantes = []
    for tabla in Base.metadata.sorted_tables:
        existentes = {c["name"] for c in inspector.get_columns(tabla.name)}
        faltantes += [f"{tabla.name}.{c.name}" for c in tabla.columns if c.name not in existentes]
    if faltantes:
        raise EsquemaIncompatibleError(
            "La base SQLite no coincide con los modelos; faltan columnas: "
            + ", ".join(faltantes)
            + ". Con datos sintéticos, detenga el servidor y ejecute desde backend "
            "`python -m app.core.reset_db` (respalda y recrea la base)."
        )


def init_db() -> None:
    from app.services.auth_service import bootstrap_from_environment

    verificar_esquema(engine)
    db = SessionLocal()
    try:
        bootstrap_from_environment(db)
    finally:
        db.close()
