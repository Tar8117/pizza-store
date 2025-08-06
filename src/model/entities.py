from enum import Enum
from typing import List, Optional
from uuid import UUID


class OrderStatus(Enum):
    NEW = "NEW"
    ORDERED = "ORDERED"
    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERING = "DELIVERING"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"


class Pizza:
    def __init__(self, pizza_id: Optional[UUID], base_pizza_id: UUID, topping_ids: List[UUID]):
        self.pizza_id = pizza_id
        self.base_pizza_id = base_pizza_id
        self.topping_ids = topping_ids


class User:
    def __init__(self, user_id: UUID,  name: str, phone_number: str):
        self.user_id = user_id
        self.name = name
        self.phone_number = phone_number


class Order:
    def __init__(self, order_id: UUID, status: OrderStatus, user: User, pizzas: List[Pizza], address: str = ""):
        self.order_id = order_id
        self.status = status
        self.user = user
        self.pizzas = pizzas
        self.address = address


class BasePizza:
    def __init__(self, base_pizza_id: UUID, name: str, price: float):
        self.base_pizza_id = base_pizza_id
        self.name = name
        self.price = price


class Topping:
    def __init__(self, topping_id: UUID, name: str, price: float):
        self.topping_id = topping_id
        self.name = name
        self.price = price
