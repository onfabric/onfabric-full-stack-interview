from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == "ok"


def test_db_health_endpoint(client: TestClient):
    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
