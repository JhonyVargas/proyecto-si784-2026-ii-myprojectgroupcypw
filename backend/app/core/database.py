"""Configuración de la base de datos SQLite del prototipo NotaryVerify."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{(DATA_DIR / 'notaryverify.db').as_posix()}"

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


def init_db() -> None:
    from app.models import db_models  # noqa: F401 (registra las tablas en Base.metadata)
    from app.services.auth_service import bootstrap_from_environment

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        bootstrap_from_environment(db)
    finally:
        db.close()
