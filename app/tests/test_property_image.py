from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_delete_property_image():
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

    image_data = {
        "image_url": "https://example.com/image1.jpg",
        "is_primary": True,
    }
    response = client.post(
        f"/api/property-images/{listing_id}",
        json=image_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["image_url"] == image_data["image_url"]
    assert data["is_primary"] is True
    image_id = data["id"]

    response = client.get(f"/api/property-images/listing/{listing_id}")
    assert response.status_code == 200
    images = response.json()
    assert len(images) >= 1
    assert any(img["id"] == image_id for img in images)

    response = client.delete(
        f"/api/property-images/{image_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204