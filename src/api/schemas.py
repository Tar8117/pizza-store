from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field
from model.entities import OrderStatus, Pizza


class UserCreate(BaseModel):
    name: str
    phone_number: str = Field(..., example="+79001234567")


class UserOut(BaseModel):
    user_id: UUID
    name: str
    phone_number: str


class PizzaIn(BaseModel):
    base_pizza_id: UUID
    topping_ids: List[UUID]


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
