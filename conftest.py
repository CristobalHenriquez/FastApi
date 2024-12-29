import pytest
from fastapi.testclient import TestClient
from app.main import app  # Reemplaza con el archivo principal de tu aplicación
from app.database import Base, engine, SessionLocal

# Crea una base de datos de prueba
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)  # Crea las tablas
    yield SessionLocal()  # Proporciona una sesión para las pruebas
    Base.metadata.drop_all(bind=engine)  # Elimina las tablas después de las pruebas

# Cliente de prueba para interactuar con la API
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
