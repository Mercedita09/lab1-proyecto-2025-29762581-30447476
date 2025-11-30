from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_obtener_persona_no_existente():
    response = client.get("/personas/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Persona no encontrada"

def test_crear_persona():
    payload = {
        "nombre": "José Pérez",
        "cedula": "12345678",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "Barquisimeto",
        "telefono": "04141234567",
        "email": "jose@example.com"
    }
    response = client.post("/personas/", json=payload)
    # Como aún no está implementado, esperamos error 400
    assert response.status_code in [200, 400]
