import pytest

from fastapi import HTTPException

from app.core.dependencies import require_roles
from app.models.user import User


# --------------------------------------------------
# TEST USERS
# --------------------------------------------------

@pytest.fixture
def admin_user():
    return User(
        id=1,
        username="test_admin",
        email="admin@test.com",
        password_hash="test_hash",
        role="admin",
    )


@pytest.fixture
def manager_user():
    return User(
        id=2,
        username="test_manager",
        email="manager@test.com",
        password_hash="test_hash",
        role="manager",
    )


@pytest.fixture
def employee_user():
    return User(
        id=3,
        username="test_employee",
        email="employee@test.com",
        password_hash="test_hash",
        role="employee",
    )


# --------------------------------------------------
# RBAC HELPER
# --------------------------------------------------

def check_role(user, *allowed_roles):
    role_checker = require_roles(*allowed_roles)
    return role_checker(current_user=user)


# --------------------------------------------------
# PRODUCTS
# Read: All
# Create/Update/Delete: Admin
# --------------------------------------------------

@pytest.mark.parametrize(
    "role",
    ["admin", "manager", "employee"],
)
def test_all_roles_can_read_products(
    role,
    admin_user,
    manager_user,
    employee_user,
):
    users = {
        "admin": admin_user,
        "manager": manager_user,
        "employee": employee_user,
    }

    result = check_role(
        users[role],
        "admin",
        "manager",
        "employee",
    )

    assert result.role == role


@pytest.mark.parametrize(
    "role",
    ["manager", "employee"],
)
def test_only_admin_can_modify_products(
    role,
    manager_user,
    employee_user,
):
    users = {
        "manager": manager_user,
        "employee": employee_user,
    }

    with pytest.raises(HTTPException) as exc:
        check_role(users[role], "admin")

    assert exc.value.status_code == 403


def test_admin_can_modify_products(admin_user):
    result = check_role(admin_user, "admin")

    assert result.role == "admin"


# --------------------------------------------------
# WAREHOUSES
# Read: All
# Create/Update/Delete: Admin
# --------------------------------------------------

@pytest.mark.parametrize(
    "role",
    ["manager", "employee"],
)
def test_only_admin_can_modify_warehouses(
    role,
    manager_user,
    employee_user,
):
    users = {
        "manager": manager_user,
        "employee": employee_user,
    }

    with pytest.raises(HTTPException) as exc:
        check_role(users[role], "admin")

    assert exc.value.status_code == 403


# --------------------------------------------------
# INVENTORY
# Read: All
# Create/Update: Admin, Manager
# Delete: Admin
# --------------------------------------------------

@pytest.mark.parametrize(
    "role",
    ["admin", "manager"],
)
def test_admin_and_manager_can_modify_inventory(
    role,
    admin_user,
    manager_user,
):
    users = {
        "admin": admin_user,
        "manager": manager_user,
    }

    result = check_role(
        users[role],
        "admin",
        "manager",
    )

    assert result.role == role


def test_employee_cannot_modify_inventory(employee_user):
    with pytest.raises(HTTPException) as exc:
        check_role(
            employee_user,
            "admin",
            "manager",
        )

    assert exc.value.status_code == 403


def test_only_admin_can_delete_inventory(
    admin_user,
    manager_user,
    employee_user,
):
    assert check_role(admin_user, "admin").role == "admin"

    for user in [manager_user, employee_user]:
        with pytest.raises(HTTPException) as exc:
            check_role(user, "admin")

        assert exc.value.status_code == 403


# --------------------------------------------------
# ORDERS
# Read/Create: All
# Update: Admin, Manager
# Delete: Admin
# --------------------------------------------------

@pytest.mark.parametrize(
    "role",
    ["admin", "manager", "employee"],
)
def test_all_roles_can_create_orders(
    role,
    admin_user,
    manager_user,
    employee_user,
):
    users = {
        "admin": admin_user,
        "manager": manager_user,
        "employee": employee_user,
    }

    result = check_role(
        users[role],
        "admin",
        "manager",
        "employee",
    )

    assert result.role == role


@pytest.mark.parametrize(
    "role",
    ["admin", "manager"],
)
def test_admin_and_manager_can_update_orders(
    role,
    admin_user,
    manager_user,
):
    users = {
        "admin": admin_user,
        "manager": manager_user,
    }

    result = check_role(
        users[role],
        "admin",
        "manager",
    )

    assert result.role == role


def test_employee_cannot_update_orders(employee_user):
    with pytest.raises(HTTPException) as exc:
        check_role(employee_user, "admin", "manager")

    assert exc.value.status_code == 403


def test_only_admin_can_delete_orders(
    admin_user,
    manager_user,
    employee_user,
):
    assert check_role(admin_user, "admin").role == "admin"

    for user in [manager_user, employee_user]:
        with pytest.raises(HTTPException) as exc:
            check_role(user, "admin")

        assert exc.value.status_code == 403