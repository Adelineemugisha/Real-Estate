from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "fully_modular_architecture_online"}


def test_register_user():
    import time
    user_data = {
        "email": f"test_register_{int(time.time())}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "role": "buyer",
    }
    response = client.post("/api/user/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["role"] == user_data["role"]
    assert "password" not in data
    return data["id"]


def test_login_user():
    import time
    user_data = {
        "email": f"test_login_{int(time.time())}@example.com",
        "first_name": "Test",
        "last_name": "Login",
        "password": "testpass123",
        "role": "buyer",
    }
    response = client.post("/api/user/register", json=user_data)
    assert response.status_code == 201
    response = client.post("/api/user/login", json={
        "email": user_data["email"],
        "password": user_data["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]


def test_get_current_user():
    import time
    user_data = {
        "email": f"test_get_current_{int(time.time())}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "role": "buyer",
    }
    client.post("/api/user/register", json=user_data)
    login_response = client.post("/api/user/login", json={
        "email": user_data["email"],
        "password": user_data["password"],
    })
    token = login_response.json()["access_token"]

    response = client.get(
        "/api/user/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]


def test_update_user():
    import time
    user_data = {
        "email": f"test_update_{int(time.time())}@example.com",
        "first_name": "Update",
        "last_name": "Test",
        "password": "testpass123",
        "role": "buyer",
    }
    response = client.post("/api/user/register", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    login_response = client.post("/api/user/login", json={
        "email": user_data["email"],
        "password": user_data["password"],
    })
    token = login_response.json()["access_token"]

    update_data = {"first_name": "Updated", "last_name": "Name"}
    response = client.put(
        f"/api/user/{user_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"


def test_delete_user():
    import time
    user_data = {
        "email": f"test_delete_{int(time.time())}@example.com",
        "first_name": "Delete",
        "last_name": "Test",
        "password": "testpass123",
        "role": "buyer",
    }
    response = client.post("/api/user/register", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    login_response = client.post("/api/user/login", json={
        "email": user_data["email"],
        "password": user_data["password"],
    })
    token = login_response.json()["access_token"]

    response = client.delete(
        f"/api/user/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204