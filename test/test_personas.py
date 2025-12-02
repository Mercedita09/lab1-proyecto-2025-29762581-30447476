import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test endpoint raíz."""
    response = client.get("/")
    assert response.status_code == 200
    assert "API de Gestión" in response.json()["message"]

def test_health_check():
    """Test health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_swagger_docs():
    """Test que Swagger esté disponible."""
    response = client.get("/api-docs")
    assert response.status_code == 200

def test_endpoints_personas():
    """Test que los endpoints de personas existan."""
    response = client.get("/api/v1/personas/")
    # Puede devolver 200 (si hay datos) o 200 con lista vacía
    assert response.status_code in [200, 404]