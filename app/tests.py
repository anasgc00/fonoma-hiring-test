import pytest
from .models import Order, Status
from .validators import validate_criterion
from .main import app
from fastapi.testclient import TestClient

# Testing Order model


def test_order_create():
    order = Order(id=1, item="Test", quantity=2,
                  price=9.0, status=Status.completed)
    assert (order.id == 1)
    assert (order.item == "Test")
    assert (order.quantity == 2)
    assert (order.price == 9.0)
    assert (order.status == "completed")


def test_order_price_validation():
    with pytest.raises(ValueError):
        Order(id=1, item="Test", quantity=2,
              price=-9.0, status=Status.completed)

# Testing validate_criterion


def test_validate_criterion():
    assert (validate_criterion("x") == False)

# Testing /solution endpoint


def test_solution_endpoint():
    client = TestClient(app)
    response = client.post(
        "/solution/",
        headers={"Content-Type": "application/json"},
        json={
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1,
                 "price": 999.99, "status": "completed"},
                {"id": 2, "item": "Smartphone", "quantity": 2,
                 "price": 499.95, "status": "pending"},
                {"id": 3, "item": "Headphones", "quantity": 3,
                 "price": 99.90, "status": "completed"},
                {"id": 4, "item": "Mouse", "quantity": 4,
                 "price": 24.99, "status": "canceled"},
            ],
            "criterion": "completed"
        }
    )
    assert (response.status_code == 200)
    print(response.json() == {
        "revenue": 1099.89
    })


def test_solution_endpoint_invalid_criterion():
    client = TestClient(app)
    response = client.post(
        "/solution/",
        headers={"Content-Type": "application/json"},
        json={
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1,
                 "price": 999.99, "status": "completed"},
                {"id": 2, "item": "Smartphone", "quantity": 2,
                 "price": 499.95, "status": "pending"},
                {"id": 3, "item": "Headphones", "quantity": 3,
                 "price": 99.90, "status": "completed"},
                {"id": 4, "item": "Mouse", "quantity": 4,
                 "price": 24.99, "status": "canceled"},
            ],
            "criterion": "asdad"
        }
    )
    assert (response.status_code == 400)


def test_solution_endpoint_invalid_order_price():
    client = TestClient(app)
    response = client.post(
        "/solution/",
        headers={"Content-Type": "application/json"},
        json={
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1,
                 "price": 999.99, "status": "completed"},
                {"id": 2, "item": "Smartphone", "quantity": 2,
                 "price": -499.95, "status": "pending"},
                {"id": 3, "item": "Headphones", "quantity": 3,
                 "price": 99.90, "status": "completed"},
                {"id": 4, "item": "Mouse", "quantity": 4,
                 "price": 24.99, "status": "canceled"},
            ],
            "criterion": "completed"
        }
    )
    assert (response.status_code == 422)
