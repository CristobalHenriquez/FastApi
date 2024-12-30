import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal

# Crear un cliente de pruebas
@pytest.fixture(scope="module")
def client():
    # Crear las tablas en una base de datos en memoria (si es SQLite o temporal para pruebas)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Eliminar las tablas al final de las pruebas
    Base.metadata.drop_all(bind=engine)

# Crear una sesión de base de datos para pruebas
@pytest.fixture(scope="function")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_crear_provincia(client):
    payload = {"nombre": "Provincia de Prueba"}
    response = client.post("/provincias/", json=payload)
    assert response.status_code == 201
    assert response.json()["nombre"] == "Provincia De Prueba"

def test_obtener_provincias(client):
    # Asegúrate de que hay al menos una provincia
    client.post("/provincias/", json={"nombre": "Provincia de Ejemplo"})
    response = client.get("/provincias/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Verifica que haya provincias

def test_actualizar_provincia(client):
    # Crear una provincia para actualizar
    create_response = client.post("/provincias/", json={"nombre": "Provincia para Actualizar"})
    assert create_response.status_code == 201
    provincia_id = create_response.json()["id_provincia"]

    # Actualizar la provincia
    payload = {"nombre": "Provincia Actualizada"}
    response = client.put(f"/provincias/{provincia_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Provincia Actualizada"

def test_eliminar_provincia(client):
    # Crear una provincia para eliminar
    create_response = client.post("/provincias/", json={"nombre": "Provincia para Eliminar"})
    assert create_response.status_code == 201
    provincia_id = create_response.json()["id_provincia"]

    # Eliminar la provincia
    response = client.delete(f"/provincias/{provincia_id}")
    assert response.status_code == 204

    # Verifica que la provincia fue eliminada
    response = client.get(f"/provincias/{provincia_id}")
    assert response.status_code == 404
