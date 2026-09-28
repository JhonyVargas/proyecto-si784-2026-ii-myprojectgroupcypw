import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models import db_models  # noqa: F401 (registra las tablas en Base.metadata)


@pytest.fixture()
def db_session():
    """Sesión de base de datos SQLite en memoria, aislada por cada prueba."""

    # TestClient ejecuta dependencias en otro hilo. StaticPool mantiene la misma
    # base en memoria para que las pruebas HTTP vean las tablas del fixture.
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()
