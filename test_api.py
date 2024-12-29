import requests

BASE_URL = "http://127.0.0.1:8000"  # Cambia esto si tu API está desplegada en otro lugar.

def test_crear_provincia():
    url = f"{BASE_URL}/provincias/"
    payload = {"nombre": "Provincia Test"}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Provincia Test"

def test_leer_provincias():
    url = f"{BASE_URL}/provincias/"
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
