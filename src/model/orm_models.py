from sqlalchemy import Column, String, Float, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from enum import Enum
from typing import Annotated, List, Optional


uuid_pk = Annotated[str, mapped_column(primary_key=True)]


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


pizza_topping = Table(
    "pizza_topping",
    Base.metadata,
    Column("pizza_id", ForeignKey("pizzas.pizza_id"), primary_key=True),
    Column("topping_id", ForeignKey("toppings.topping_id"), primary_key=True),
)


class UserOrm(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid_pk]
    name: Mapped[str]
    phone_number: Mapped[str]
    orders: Mapped[List["OrderOrm"]] = relationship("OrderOrm", back_populates="user")


class OrderOrm(Base):
    __tablename__ = "orders"

    order_id: Mapped[uuid_pk]
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))  # type: ignore
    address: Mapped[str]
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="orders")
    pizzas: Mapped[List["PizzaOrm"]] = relationship("PizzaOrm", back_populates="order")


class PizzaOrm(Base):
    __tablename__ = "pizzas"

    pizza_id: Mapped[uuid_pk]
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.order_id"))
    order: Mapped["OrderOrm"] = relationship("OrderOrm", back_populates="pizzas")
    base_pizza_id: Mapped[str] = mapped_column(ForeignKey("base_pizzas.base_pizza_id"))
    base_pizza: Mapped["BasePizzaOrm"] = relationship("BasePizzaOrm")
    toppings: Mapped[List["ToppingOrm"]] = relationship(
        "ToppingOrm", secondary=pizza_topping, back_populates="pizzas"
    )


class BasePizzaOrm(Base):
    __tablename__ = "base_pizzas"

    base_pizza_id: Mapped[uuid_pk]
    name: Mapped[str]
    price: Mapped[float]


class ToppingOrm(Base):
    __tablename__ = "toppings"

    topping_id: Mapped[uuid_pk]
    name: Mapped[str]
    price: Mapped[float]
    pizzas: Mapped[List[PizzaOrm]] = relationship(
        "PizzaOrm", secondary=pizza_topping, back_populates="toppings"
    )
