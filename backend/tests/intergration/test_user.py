from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models


def test_read_user(client: TestClient, api_key: models.ApiKey):
    response = client.get("/user", headers={"X-API-Key": api_key.key})
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["fullname"] == "Test User" 
    assert data["nickname"] == "tester"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_update_user(client: TestClient, db: Session, api_key: models.ApiKey):
    update_data = {
        "email": "updated@example.com",
        "fullname": "Updated User",
        "nickname": "updated"
    }

    response = client.put("/user", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == update_data["email"]
    assert data["fullname"] == update_data["fullname"]
    assert data["nickname"] == update_data["nickname"]

    # Verify changes in database
    user = db.query(models.User).filter(models.User.id == data["id"]).first()
    assert user.email == update_data["email"]
    assert user.fullname == update_data["fullname"]
    assert user.nickname == update_data["nickname"]



def test_read_user_keys(client: TestClient, db: Session, api_key: models.ApiKey):
    response = client.get("/user/keys", headers={"X-API-Key": api_key.key})
    assert response.status_code == 200


def test_create_user_key(client: TestClient, db: Session, api_key: models.ApiKey):
    key_data = {
        "name": "New Key"
    }
    response = client.post("/user/keys", json=key_data, headers={"X-API-Key": api_key.key})
    assert response.status_code == 200, response.json()
    
    data = response.json()
    assert data["name"] == key_data["name"]
    assert "key" in data
    assert "id" in data

    # Verify key was created in database
    db_key = db.query(models.ApiKey).filter(models.ApiKey.id == data["id"]).first()
    assert db_key is not None
    assert db_key.name == key_data["name"]


def test_read_user_key(client: TestClient, api_key: models.ApiKey):
    response = client.get(f"/user/keys/{api_key.id}", headers={"X-API-Key": api_key.key})
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == api_key.id
    assert data["key"] == api_key.key
    assert data["name"] == api_key.name


def test_delete_user_key(client: TestClient, db: Session, api_key: models.ApiKey):
    # Create a new key to delete
    key_to_delete = models.ApiKey(
        user_id=api_key.user_id,
        key=str(uuid4()),
        name="Key to Delete"
    )
    db.add(key_to_delete)
    db.commit()
    db.refresh(key_to_delete)

    response = client.delete(f"/user/keys/{key_to_delete.id}", headers={"X-API-Key": api_key.key})
    assert response.status_code == 200

    # Verify key was deleted
    deleted_key = db.query(models.ApiKey).filter(models.ApiKey.id == key_to_delete.id).first()
    assert deleted_key is None


def test_read_user_requests(client: TestClient, db: Session, api_key: models.ApiKey):
    # Create test requests
    requests = [
        models.UserRequest(
            key_id=api_key.id,
            endpoint="/test",
            method="GET",
            status_code=200
        )
        for _ in range(3)
    ]
    for request in requests:
        db.add(request)
    db.commit()

    response = client.get(f"/user/keys/{api_key.id}/requests", headers={"X-API-Key": api_key.key})
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
