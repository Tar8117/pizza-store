from uuid import UUID, uuid4
from typing import List
from pydantic import BaseModel
from model.entities import OrderStatus, Pizza


class UserCreate(BaseModel):
    name: str
    phone_number: str


class UserOut(BaseModel):
    user_id: UUID
    name: str
    phone_number: str


class PizzaIn(BaseModel):
    base_pizza_id: UUID
    topping_ids: List[UUID]

    def to_entity(self) -> Pizza:
        return Pizza(
            pizza_id=None,
            base_pizza_id=self.base_pizza_id,
            topping_ids=self.topping_ids
        )


class AddressUpdate(BaseModel):
    address: str


class OrderOut(BaseModel):
    order_id: UUID
    status: OrderStatus
    address: str
    user: UserOut
    pizzas: List[PizzaIn]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
