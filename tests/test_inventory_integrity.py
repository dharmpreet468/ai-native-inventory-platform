from uuid import uuid4


def create_test_product(client):
    name = f"Day6 Product {uuid4().hex[:8]}"

    response = client.post(
        "/products/",
        json={
            "name": name,
            "price": 100.0,
            "category": "Day6-Test",
        },
    )

    assert response.status_code == 200
    return response.json()["id"]


def create_test_warehouse(client):
    name = f"Day6 Warehouse {uuid4().hex[:8]}"

    response = client.post(
        "/warehouses/",
        json={
            "name": name,
            "location": "Day6-Test",
        },
    )

    assert response.status_code == 200
    return response.json()["id"]


def test_inventory_lifecycle(authenticated_client):
    client = authenticated_client

    product_id = create_test_product(client)
    warehouse_id = create_test_warehouse(client)

    # 1. Create inventory
    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "quantity": 100,
        },
    )

    assert response.status_code == 200

    inventory = response.json()
    inventory_id = inventory["id"]

    assert inventory["product_id"] == product_id
    assert inventory["warehouse_id"] == warehouse_id
    assert inventory["quantity"] == 100

    # 2. Duplicate inventory must fail
    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "quantity": 50,
        },
    )

    assert response.status_code == 409

    # 3. PATCH quantity
    response = client.patch(
        f"/inventories/{inventory_id}",
        json={
            "quantity": 80,
        },
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 80

    # 4. PUT inventory
    response = client.put(
        f"/inventories/{inventory_id}",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "quantity": 120,
        },
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 120

    # 5. Verify persistence
    response = client.get(
        f"/inventories/{inventory_id}"
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 120

    # 6. DELETE inventory
    response = client.delete(
        f"/inventories/{inventory_id}"
    )

    assert response.status_code == 204

    # 7. Verify deletion
    response = client.get(
        f"/inventories/{inventory_id}"
    )

    assert response.status_code == 404


def test_order_insufficient_inventory_rolls_back(authenticated_client):
    client = authenticated_client

    product_id = create_test_product(client)

    warehouse_1 = create_test_warehouse(client)
    warehouse_2 = create_test_warehouse(client)

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_1,
            "quantity": 60,
        },
    )

    assert response.status_code == 200
    inventory_1_id = response.json()["id"]

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_2,
            "quantity": 40,
        },
    )

    assert response.status_code == 200
    inventory_2_id = response.json()["id"]

    # Total stock = 100, request = 150
    response = client.post(
        "/orders/",
        json={
            "product_id": product_id,
            "quantity": 150,
        },
    )

    assert response.status_code == 409

    # Rollback must preserve both inventory quantities
    response = client.get(
        f"/inventories/{inventory_1_id}"
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 60

    response = client.get(
        f"/inventories/{inventory_2_id}"
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 40


def test_order_allocates_across_multiple_warehouses(authenticated_client):
    client = authenticated_client

    product_id = create_test_product(client)

    warehouse_1 = create_test_warehouse(client)
    warehouse_2 = create_test_warehouse(client)

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_1,
            "quantity": 60,
        },
    )

    assert response.status_code == 200
    inventory_1_id = response.json()["id"]

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_2,
            "quantity": 40,
        },
    )

    assert response.status_code == 200
    inventory_2_id = response.json()["id"]

    # Request 75 units from total stock of 100
    response = client.post(
        "/orders/",
        json={
            "product_id": product_id,
            "quantity": 75,
        },
    )

    assert response.status_code == 200

    order = response.json()

    assert order["product_id"] == product_id
    assert order["quantity"] == 75
    assert order["status"] == "CONFIRMED"

    # Warehouse 1: 60 - 60 = 0
    response = client.get(
        f"/inventories/{inventory_1_id}"
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 0

    # Warehouse 2: 40 - 15 = 25
    response = client.get(
        f"/inventories/{inventory_2_id}"
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 25


def test_order_cancellation_restores_allocated_inventory(authenticated_client):
    client = authenticated_client

    product_id = create_test_product(client)

    warehouse_1 = create_test_warehouse(client)
    warehouse_2 = create_test_warehouse(client)

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_1,
            "quantity": 60,
        },
    )

    assert response.status_code == 200
    inventory_1_id = response.json()["id"]

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_2,
            "quantity": 40,
        },
    )

    assert response.status_code == 200
    inventory_2_id = response.json()["id"]

    # Create confirmed order for 75 units
    response = client.post(
        "/orders/",
        json={
            "product_id": product_id,
            "quantity": 75,
        },
    )

    assert response.status_code == 200

    order_id = response.json()["id"]

    assert response.json()["status"] == "CONFIRMED"

    # Verify stock was deducted
    response = client.get(
        f"/inventories/{inventory_1_id}"
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 0

    response = client.get(
        f"/inventories/{inventory_2_id}"
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 25

    # Cancel order
    response = client.delete(
        f"/orders/{order_id}"
    )

    assert response.status_code == 200

    # Verify exact restoration
    response = client.get(
        f"/inventories/{inventory_1_id}"
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 60

    response = client.get(
        f"/inventories/{inventory_2_id}"
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 40

    # Verify order is cancelled
    response = client.get(
        f"/orders/{order_id}"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"


def test_analytics_summary(authenticated_client):
    client = authenticated_client

    response = client.get("/analytics/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_products" in data
    assert "total_warehouses" in data
    assert "total_inventory_units" in data
    assert "total_orders" in data
    assert "total_order_units" in data
    assert "total_inventory_value" in data

    assert data["total_products"] >= 0
    assert data["total_warehouses"] >= 0
    assert data["total_inventory_units"] >= 0
    assert data["total_orders"] >= 0
    assert data["total_order_units"] >= 0
    assert data["total_inventory_value"] >= 0


def test_low_stock_inventory(authenticated_client):
    client = authenticated_client

    response = client.get(
        "/analytics/low-stock?threshold=20"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for item in data:
        assert "product_id" in item
        assert "warehouse_id" in item
        assert "product_name" in item
        assert "warehouse_name" in item
        assert "quantity" in item
        assert "threshold" in item

        assert item["quantity"] <= item["threshold"]