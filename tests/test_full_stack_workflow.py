import uuid


# ============================================================
# HTTP CONTRACT
# ============================================================

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_UNPROCESSABLE_ENTITY = 422


# ============================================================
# FULL-STACK BUSINESS WORKFLOW
# ============================================================

def test_full_stack_inventory_order_workflow(authenticated_client):
    """
    Full integration test:

    HTTP
      ↓
    FastAPI Router
      ↓
    Pydantic Validation
      ↓
    Service Layer
      ↓
    Repository Layer
      ↓
    SQLAlchemy
      ↓
    MySQL
      ↓
    HTTP Response

    Tests:
    - Product creation
    - Warehouse creation
    - Inventory creation
    - Inventory persistence
    - Multi-warehouse order allocation
    - Inventory deduction
    - Insufficient inventory
    - Failed transaction does not mutate inventory
    - Order cancellation
    - Inventory restoration
    - Duplicate cancellation protection
    - Analytics
    """

    client = authenticated_client

    suffix = uuid.uuid4().hex[:8]

    product_name = f"Integration Product {suffix}"
    warehouse_a_name = f"Integration Warehouse A {suffix}"
    warehouse_b_name = f"Integration Warehouse B {suffix}"

    # ========================================================
    # 1. CREATE PRODUCT
    # ========================================================

    response = client.post(
        "/products/",
        json={
            "name": product_name,
            "price": 100.0,
            "category": "Integration Test",
        },
    )

    assert response.status_code == HTTP_OK

    product = response.json()

    assert product["id"] > 0
    assert product["name"] == product_name
    assert product["price"] == 100.0
    assert product["category"] == "Integration Test"

    product_id = product["id"]

    # ========================================================
    # 2. VERIFY PRODUCT THROUGH GET
    # ========================================================

    response = client.get(
        f"/products/{product_id}"
    )

    assert response.status_code == HTTP_OK

    product_from_get = response.json()

    assert product_from_get["id"] == product_id
    assert product_from_get["name"] == product_name

    # ========================================================
    # 3. CREATE WAREHOUSE A
    # ========================================================

    response = client.post(
        "/warehouses/",
        json={
            "name": warehouse_a_name,
            "location": "Integration Test A",
        },
    )

    assert response.status_code == HTTP_OK

    warehouse_a = response.json()

    assert warehouse_a["id"] > 0
    assert warehouse_a["name"] == warehouse_a_name

    warehouse_a_id = warehouse_a["id"]

    # ========================================================
    # 4. CREATE WAREHOUSE B
    # ========================================================

    response = client.post(
        "/warehouses/",
        json={
            "name": warehouse_b_name,
            "location": "Integration Test B",
        },
    )

    assert response.status_code == HTTP_OK

    warehouse_b = response.json()

    assert warehouse_b["id"] > 0
    assert warehouse_b["name"] == warehouse_b_name

    warehouse_b_id = warehouse_b["id"]

    # ========================================================
    # 5. CREATE INVENTORY A = 50
    # ========================================================

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_a_id,
            "quantity": 50,
        },
    )

    assert response.status_code == HTTP_OK

    inventory_a = response.json()

    assert inventory_a["product_id"] == product_id
    assert inventory_a["warehouse_id"] == warehouse_a_id
    assert inventory_a["quantity"] == 50

    inventory_a_id = inventory_a["id"]

    # ========================================================
    # 6. CREATE INVENTORY B = 30
    # ========================================================

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_b_id,
            "quantity": 30,
        },
    )

    assert response.status_code == HTTP_OK

    inventory_b = response.json()

    assert inventory_b["product_id"] == product_id
    assert inventory_b["warehouse_id"] == warehouse_b_id
    assert inventory_b["quantity"] == 30

    inventory_b_id = inventory_b["id"]

    # ========================================================
    # 7. VERIFY INVENTORY
    # ========================================================

    response = client.get(
        f"/inventories/{inventory_a_id}"
    )

    assert response.status_code == HTTP_OK
    assert response.json()["quantity"] == 50

    response = client.get(
        f"/inventories/{inventory_b_id}"
    )

    assert response.status_code == HTTP_OK
    assert response.json()["quantity"] == 30

    # ========================================================
    # 8. DUPLICATE INVENTORY MUST BE REJECTED
    # ========================================================

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_a_id,
            "quantity": 10,
        },
    )

    assert response.status_code == HTTP_CONFLICT

    # ========================================================
    # 9. INVALID INVENTORY QUANTITY
    # ========================================================

    response = client.post(
        "/inventories/",
        json={
            "product_id": product_id,
            "warehouse_id": warehouse_a_id,
            "quantity": -10,
        },
    )

    assert response.status_code == HTTP_UNPROCESSABLE_ENTITY

    # ========================================================
    # 10. CREATE ORDER = 60
    #
    # Available:
    # Warehouse A = 50
    # Warehouse B = 30
    # Total = 80
    #
    # Expected:
    # A -> 50
    # B -> 10
    #
    # Remaining:
    # A -> 0
    # B -> 20
    # ========================================================

    response = client.post(
        "/orders/",
        json={
            "product_id": product_id,
            "quantity": 60,
        },
    )

    assert response.status_code == HTTP_OK

    order = response.json()

    assert order["id"] > 0
    assert order["product_id"] == product_id
    assert order["quantity"] == 60
    assert order["status"] == "CONFIRMED"

    order_id = order["id"]

    # ========================================================
    # 11. VERIFY INVENTORY DEDUCTION
    # ========================================================

    response = client.get(
        f"/inventories/{inventory_a_id}"
    )

    assert response.status_code == HTTP_OK

    inventory_a_after_order = response.json()

    assert inventory_a_after_order["quantity"] == 0
    assert inventory_a_after_order["quantity"] >= 0

    response = client.get(
        f"/inventories/{inventory_b_id}"
    )

    assert response.status_code == HTTP_OK

    inventory_b_after_order = response.json()

    assert inventory_b_after_order["quantity"] == 20
    assert inventory_b_after_order["quantity"] >= 0

    # ========================================================
    # 12. GET ORDER
    # ========================================================

    response = client.get(
        f"/orders/{order_id}"
    )

    assert response.status_code == HTTP_OK

    order_from_get = response.json()

    assert order_from_get["id"] == order_id
    assert order_from_get["status"] == "CONFIRMED"

    # ========================================================
    # 13. INSUFFICIENT INVENTORY
    #
    # Only 20 units remain.
    # Request 100.
    # ========================================================

    response = client.post(
        "/orders/",
        json={
            "product_id": product_id,
            "quantity": 100,
        },
    )

    assert response.status_code == HTTP_CONFLICT

    # ========================================================
    # 14. FAILED ORDER MUST NOT CHANGE INVENTORY
    # ========================================================

    response = client.get(
        f"/inventories/{inventory_a_id}"
    )

    assert response.status_code == HTTP_OK
    assert response.json()["quantity"] == 0

    response = client.get(
        f"/inventories/{inventory_b_id}"
    )

    assert response.status_code == HTTP_OK
    assert response.json()["quantity"] == 20

    # ========================================================
    # 15. INVALID ORDER QUANTITY
    # ========================================================

    response = client.post(
        "/orders/",
        json={
            "product_id": product_id,
            "quantity": 0,
        },
    )

    assert response.status_code == HTTP_UNPROCESSABLE_ENTITY

    response = client.post(
        "/orders/",
        json={
            "product_id": product_id,
            "quantity": -5,
        },
    )

    assert response.status_code == HTTP_UNPROCESSABLE_ENTITY

    # ========================================================
    # 16. NON-EXISTENT PRODUCT
    # ========================================================

    nonexistent_product_id = 999999999

    response = client.get(
        f"/products/{nonexistent_product_id}"
    )

    assert response.status_code == HTTP_NOT_FOUND

    # ========================================================
    # 17. NON-EXISTENT WAREHOUSE
    # ========================================================

    response = client.get(
        "/warehouses/999999999"
    )

    assert response.status_code == HTTP_NOT_FOUND

    # ========================================================
    # 18. NON-EXISTENT INVENTORY
    # ========================================================

    response = client.get(
        "/inventories/999999999"
    )

    assert response.status_code == HTTP_NOT_FOUND

    # ========================================================
    # 19. NON-EXISTENT ORDER
    # ========================================================

    response = client.get(
        "/orders/999999999"
    )

    assert response.status_code == HTTP_NOT_FOUND

    # ========================================================
    # 20. UPDATE CONFIRMED ORDER
    #
    # Confirmed orders cannot be modified.
    # ========================================================

    response = client.patch(
        f"/orders/{order_id}",
        json={
            "quantity": 10,
        },
    )

    assert response.status_code == HTTP_CONFLICT

    # ========================================================
    # 21. CANCEL ORDER
    #
    # CONFIRMED -> CANCELLED
    #
    # Inventory must be restored.
    # ========================================================

    response = client.delete(
        f"/orders/{order_id}"
    )

    assert response.status_code == HTTP_OK

    cancelled_order = response.json()

    assert cancelled_order["id"] == order_id
    assert cancelled_order["status"] == "CANCELLED"

    # ========================================================
    # 22. VERIFY INVENTORY RESTORATION
    #
    # A = 50
    # B = 30
    # ========================================================

    response = client.get(
        f"/inventories/{inventory_a_id}"
    )

    assert response.status_code == HTTP_OK
    assert response.json()["quantity"] == 50

    response = client.get(
        f"/inventories/{inventory_b_id}"
    )

    assert response.status_code == HTTP_OK
    assert response.json()["quantity"] == 30

    # ========================================================
    # 23. CANCEL SAME ORDER AGAIN
    # ========================================================

    response = client.delete(
        f"/orders/{order_id}"
    )

    assert response.status_code == HTTP_CONFLICT

    # ========================================================
    # 24. INVENTORY MUST STILL BE UNCHANGED
    # ========================================================

    response = client.get(
        f"/inventories/{inventory_a_id}"
    )

    assert response.status_code == HTTP_OK
    assert response.json()["quantity"] == 50

    response = client.get(
        f"/inventories/{inventory_b_id}"
    )

    assert response.status_code == HTTP_OK
    assert response.json()["quantity"] == 30

    # ========================================================
    # 25. ANALYTICS SUMMARY
    # ========================================================

    response = client.get(
        "/analytics/summary"
    )

    assert response.status_code == HTTP_OK

    summary = response.json()

    required_summary_fields = {
        "total_products",
        "total_warehouses",
        "total_inventory_units",
        "total_orders",
        "total_order_units",
        "total_inventory_value",
    }

    assert required_summary_fields.issubset(summary.keys())

    # ========================================================
    # 26. LOW-STOCK ANALYTICS
    # ========================================================

    response = client.get(
        "/analytics/low-stock",
        params={"threshold": 20},
    )

    assert response.status_code == HTTP_OK
    assert isinstance(response.json(), list)

    # ========================================================
    # 27. INVENTORY INSIGHTS
    # ========================================================

    response = client.get(
        "/analytics/inventory-insights",
        params={"threshold": 20},
    )

    assert response.status_code == HTTP_OK
    assert isinstance(response.json(), list)