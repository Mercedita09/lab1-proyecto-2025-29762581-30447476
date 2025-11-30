from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_obtener_persona_no_existente():
    response = client.get("/personas/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Persona no encontrada"
