from sqlalchemy import Column, String, Float, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from enum import Enum
from typing import List


class Base(DeclarativeBase):
    pass


class OrderStatus(Enum):
    NEW = 1
    ORDERED = 2
    PREPARING = 3
    READY = 4
    DELIVERING = 5
    DELIVERED = 6
    COMPLETED = 7


class PizzaOrm(Base):
    __tablename__ = "pizzas"

    pizza_id: Mapped[str] = mapped_column(primary_key=True)
