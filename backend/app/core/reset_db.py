"""Respalda y recrea la base SQLite de desarrollo (#21).

Uso, desde backend y con el servidor detenido:

    python -m app.core.reset_db

Solo para bases con datos sintéticos. Copia la base actual a
<DATA_DIR>/respaldo/notaryverify-<fecha>.db y crea una base vacía con el
esquema vigente de los modelos.
"""

from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine

from app.core.database import DATA_DIR, DATABASE_URL, ruta_sqlite, verificar_esquema


def reiniciar_base(url: str = DATABASE_URL, data_dir: Path = DATA_DIR) -> Path | None:
    """Respalda la base existente (si la hay), la recrea y devuelve la ruta del respaldo."""
    ruta = ruta_sqlite(url)
    if ruta is None:
        raise ValueError("El reinicio solo aplica a una base SQLite en archivo.")

    respaldo = None
    if ruta.exists():
        carpeta = data_dir / "respaldo"
        carpeta.mkdir(parents=True, exist_ok=True)
        respaldo = carpeta / f"notaryverify-{datetime.now():%Y%m%d-%H%M%S}.db"
        shutil.copy2(ruta, respaldo)
        ruta.unlink()

    motor = create_engine(url)
    try:
        verificar_esquema(motor)
    finally:
        motor.dispose()
    return respaldo


def main() -> int:
    respaldo = reiniciar_base()
    if respaldo:
        print(f"Respaldo creado en {respaldo}")
    print(f"Base recreada con el esquema vigente: {DATABASE_URL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
