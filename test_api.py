import requests

BASE_URL = "http://127.0.0.1:8000"  # Cambia esto si tu API está desplegada en otro lugar.

def test_crear_provincia(client):
    payload = {"nombre": "Provincia de Prueba"}
    response = client.post("/provincias/", json=payload)
    assert response.status_code == 201
    assert response.json()["nombre"] == "Provincia de Prueba"

def test_obtener_provincias(client):
    response = client.get("/provincias/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_actualizar_provincia(client):
    payload = {"nombre": "Provincia Actualizada"}
    response = client.put("/provincias/1", json=payload)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Provincia Actualizada"

def test_eliminar_provincia(client):
    response = client.delete("/provincias/1")
    assert response.status_code == 204

    # Verifica que la provincia fue eliminada
    response = client.get("/provincias/1")
    assert response.status_code == 404
