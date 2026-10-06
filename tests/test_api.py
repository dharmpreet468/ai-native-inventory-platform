from fastapi.testclient import TestClient

from app.main import app

Client = TestClient(app)

def test_health_check():
    response = Client.get("/health")
    
    assert response.status_code == 200