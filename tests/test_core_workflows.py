from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200


def test_create_product(authenticated_client):
    response = authenticated_client.post(
        "/products/",
        json={
            "name": "Test Product Day6",
            "price": 100.0,
            "category": "Testing",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Product Day6"
    assert data["price"] == 100.0
    assert data["category"] == "Testing"


def test_create_warehouse(authenticated_client):
    response = authenticated_client.post(
        "/warehouses/",
        json={
            "name": "Test Warehouse Day6",
            "location": "Testing",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Warehouse Day6"
    assert data["location"] == "Testing"


def test_negative_inventory_quantity_rejected(authenticated_client):
    response = authenticated_client.post(
        "/inventories/",
        json={
            "product_id": 999999,
            "warehouse_id": 999999,
            "quantity": -10,
        },
    )

    assert response.status_code == 422


def test_nonexistent_inventory_returns_404(authenticated_client):
    response = authenticated_client.get("/inventories/999999")

    assert response.status_code == 404


def test_nonexistent_product_returns_404(authenticated_client):
    response = authenticated_client.get("/products/999999")

    assert response.status_code == 404


def test_nonexistent_warehouse_returns_404(authenticated_client):
    response = authenticated_client.get("/warehouses/999999")

    assert response.status_code == 404