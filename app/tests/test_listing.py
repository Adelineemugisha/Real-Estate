from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_listing():
    import time
    user_data = {
        "email": f"test_agent_{int(time.time())}@example.com",
        "first_name": "Agent",
        "last_name": "Test",
        "password": "testpass123",
        "role": "agent",
    }
    client.post("/api/user/register", json=user_data)
    login_response = client.post("/api/user/login", json={
        "email": user_data["email"],
        "password": user_data["password"],
    })
    token = login_response.json()["access_token"]

    listing_data = {
        "title": "Modern Apartment in Kigali",
        "description": "Beautiful 2-bedroom apartment",
        "price": 500000,
        "property_type": "apartment",
        "listing_type": "sale",
        "bedrooms": 2,
        "bathrooms": 2.0,
        "square_footage": 120,
        "location": {
            "country": "Rwanda",
            "street_address": "KK 322 St",
            "city": "Kigali",
            "state_province": "Kicukiro",
            "postal_code": "0000",
            "latitude": 0,
            "longitude": 0,
        },
        "images": [],
    }
    response = client.post(
        "/api/listings/",
        json=listing_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == listing_data["title"]
    assert data["property_type"] == listing_data["property_type"]
    assert data["listing_type"] == listing_data["listing_type"]
    assert data["is_published"] is True
    assert data["id"] > 0


def test_get_listing():
    import time
    user_data = {
        "email": f"test_agent_{int(time.time())}@example.com",
        "first_name": "Agent",
        "last_name": "Test",
        "password": "testpass123",
        "role": "agent",
    }
    client.post("/api/user/register", json=user_data)
    login_response = client.post("/api/user/login", json={
        "email": user_data["email"],
        "password": user_data["password"],
    })
    token = login_response.json()["access_token"]

    listing_data = {
        "title": "Modern Apartment in Kigali",
        "description": "Beautiful 2-bedroom apartment",
        "price": 500000,
        "property_type": "apartment",
        "listing_type": "sale",
        "bedrooms": 2,
        "bathrooms": 2.0,
        "square_footage": 120,
        "location": {
            "country": "Rwanda",
            "street_address": "KK 322 St",
            "city": "Kigali",
            "state_province": "Kicukiro",
            "postal_code": "0000",
            "latitude": 0,
            "longitude": 0,
        },
        "images": [],
    }
    response = client.post(
        "/api/listings/",
        json=listing_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    listing_id = response.json()["id"]

    response = client.get(f"/api/listings/{listing_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == listing_id
    assert data["location"]["city"] == "Kigali"


def test_get_all_listings():
    response = client.get("/api/listings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)