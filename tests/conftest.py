import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.deps import get_db
from app.main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Crea las tablas antes de cada test y las elimina al finalizar,
    para que cada prueba corra sobre una base de datos limpia."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """Registra e inicia sesión con un usuario de prueba, devolviendo
    el header de autorización listo para usar en peticiones protegidas."""
    client.post(
        "/auth/register", json={"username": "vet_test", "password": "SecurePass123"}
    )
    response = client.post(
        "/auth/login",
        data={"username": "vet_test", "password": "SecurePass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
