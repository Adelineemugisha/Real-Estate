from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_location():
    import time
    agent_data = {
        "email": f"test_agent_{int(time.time())}@example.com",
        "first_name": "Agent",
        "last_name": "Test",
        "password": "testpass123",
        "role": "agent",
    }
    client.post("/api/user/register", json=agent_data)
    login_response = client.post("/api/user/login", json={
        "email": agent_data["email"],
        "password": agent_data["password"],
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
    listing_response = client.post(
        "/api/listings/",
        json=listing_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    listing_id = listing_response.json()["id"]

    response = client.get(f"/api/locations/{listing_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["listing_id"] == listing_id
    assert data["city"] == "Kigali"
    assert data["country"] == "Rwanda"
    assert data["state_province"] == "Kicukiro"