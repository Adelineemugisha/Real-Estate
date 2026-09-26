"""CRUD tests for the Listings endpoint.

Covers:
- Successful creation happy path (POST /api/listings/)
- Validation error on missing required fields (POST /api/listings/)
- 404 missing resource (GET /api/listings/{invalid_id})
"""

import time
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def agent_token(client: TestClient) -> str:
    """Register and log in an agent, returning a JWT access token."""
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
    return login_response.json()["access_token"]


@pytest.fixture
def buyer_token(client: TestClient) -> str:
    """Register and log in a buyer, returning a JWT access token."""
    buyer_data = {
        "email": f"test_buyer_{int(time.time())}@example.com",
        "first_name": "Buyer",
        "last_name": "Test",
        "password": "testpass123",
        "role": "buyer",
    }
    client.post("/api/user/register", json=buyer_data)
    login_response = client.post("/api/user/login", json={
        "email": buyer_data["email"],
        "password": buyer_data["password"],
    })
    return login_response.json()["access_token"]


def test_create_listing_success(client: TestClient, agent_token: str):
    """Happy path: an authenticated agent creates a listing and receives 201."""
    listing_data = {
        "title": "Modern Apartment in Kigali",
        "description": "Beautiful 2-bedroom apartment with city views",
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
            "latitude": -1.95,
            "longitude": 30.05,
        },
        "images": [],
    }
    response = client.post(
        "/api/listings/",
        json=listing_data,
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == listing_data["title"]
    assert float(data["price"]) == 500000.0
    assert data["property_type"] == "apartment"
    assert data["listing_type"] == "sale"
    assert data["agent_id"] is not None
    assert data["location"]["city"] == "Kigali"
    assert "id" in data


def test_create_listing_validation_error(client: TestClient, agent_token: str):
    """Validation failure: missing required 'title' field returns 422."""
    invalid_listing = {
        "description": "Missing title",
        "price": 100000,
        "property_type": "house",
        "listing_type": "sale",
        "location": {
            "country": "Rwanda",
            "street_address": "Main St",
            "city": "Kigali",
            "state_province": "Kigali",
        },
    }
    response = client.post(
        "/api/listings/",
        json=invalid_listing,
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 422


def test_get_listing_not_found(client: TestClient):
    """404 scenario: requesting a non-existent listing ID returns 404."""
    response = client.get("/api/listings/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Listing not found"


def test_list_all_listings_empty(client: TestClient, agent_token: str):
    """GET /api/listings/ returns an empty list when no listings exist."""
    response = client.get("/api/listings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)