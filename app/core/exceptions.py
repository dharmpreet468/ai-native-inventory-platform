class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product {product_id} not found")


class WarehouseNotFoundException(Exception):
    def __init__(self, warehouse_id: int):
        self.warehouse_id = warehouse_id
        super().__init__(f"Warehouse {warehouse_id} not found")


class InventoryNotFoundException(Exception):
    def __init__(self, inventory_id: int):
        self.inventory_id = inventory_id
        super().__init__(f"Inventory {inventory_id} not found")


class OrderNotFoundException(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(f"Order {order_id} not found")


class InsufficientInventory(Exception):
    def __init__(self, product_id: int, requested: int, available: int):

        self.product_id = product_id
        self.requested = requested
        self.available = available

        super().__init__(
            f"Insufficient Inventory for product {product_id}. "
            f"Requested: {requested}, Available: {available}. "
        )


class DuplicateProductException(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Product {name} already exists.")


class DuplicateWarehouseException(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Warehouse {name} already exists.")


class ProductHasInventoryException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(
            f"Product {product_id} cannot be deleted because inventory exists"
        )


class WarehouseHasInventoryException(Exception):
    def __init__(self, warehouse_id: int):
        self.warehouse_id = warehouse_id
        super().__init__(
            f"Warehouse {warehouse_id} cannot be deleted because inventory exists"
        )


class ProductHasOrderException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product {product_id} cannot be deleted because order exists")


class InventoryAlreadyExistsException(Exception):
    def __init__(self, product_id: int, warehouse_id: int):
        self.product_id = product_id
        self.warehouse_id = warehouse_id

        super().__init__(
            f"Inventory already exists for product {product_id} "
            f"in warehouse {warehouse_id}"
        )


class CancelledOrderException(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id

        super().__init__(f"Order {order_id} is already cancelled")


class OrderAlreadyConfirmedException(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(
            f"Order {order_id} is already confirmed and cannot be modified"
        )


class UsernameAlreadyExistedException(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Username {username} already exists")


class EmailAlreadyExistedException(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email {email} already exists")


class InvalidUsernamePasswordException(Exception):
    def __init__(self):
        super().__init__(f"Invalid username or password")
