from sqlalchemy import Column, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from enum import Enum as EnumPy
from typing import Annotated, List
# from .entities import User, Order, Pizza, BasePizza, Topping
from uuid import UUID


uuid_pk = Annotated[UUID, mapped_column(UUID_DB(as_uuid=True), primary_key=True)]


class Base(DeclarativeBase):
    pass


class OrderStatus(EnumPy):
    NEW = "NEW"
    ORDERED = "ORDERED"
    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERING = "DELIVERING"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"


pizza_topping = Table(
    "pizza_topping",
    Base.metadata,
    Column("pizza_id", ForeignKey("pizzas.pizza_id", ondelete="CASCADE"), primary_key=True),
    Column("topping_id", ForeignKey("toppings.topping_id", ondelete="CASCADE"), primary_key=True),
)


class UserOrm(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    orders: Mapped[List["OrderOrm"]] = relationship(
        "OrderOrm",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<UserOrm(user_id={self.user_id}, name={self.name})>"


class OrderOrm(Base):
    __tablename__ = "orders"

    order_id: Mapped[uuid_pk]
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, native_enum=False))
    address: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    user: Mapped["UserOrm"] = relationship(
        "UserOrm",
        back_populates="orders",
        passive_deletes=True,
    )
    pizzas: Mapped[List["PizzaOrm"]] = relationship(
        "PizzaOrm",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return (f"<OrderOrm(order_id={self.order_id}, status={self.status}, user={self.user}, user_id={self.user_id},"
                f"pizzas={self.pizzas}, address={self.address})>")


class PizzaOrm(Base):
    __tablename__ = "pizzas"

    pizza_id: Mapped[uuid_pk]
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.order_id", ondelete="CASCADE"))
    order: Mapped["OrderOrm"] = relationship(
        "OrderOrm",
        back_populates="pizzas",
        passive_deletes=True,
    )
    base_pizza_id: Mapped[UUID] = mapped_column(ForeignKey("base_pizzas.base_pizza_id", ondelete="CASCADE"))
    base_pizza: Mapped["BasePizzaOrm"] = relationship(
        "BasePizzaOrm",
        back_populates="pizzas",
        passive_deletes=True,
    )
    toppings: Mapped[List["ToppingOrm"]] = relationship(
        "ToppingOrm",
        secondary=pizza_topping,
        back_populates="pizzas",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<PizzaOrm(pizza_id={self.pizza_id})>"


class BasePizzaOrm(Base):
    __tablename__ = "base_pizzas"

    base_pizza_id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    pizzas: Mapped[List["PizzaOrm"]] = relationship(
        "PizzaOrm",
        back_populates="base_pizza",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<BasePizzaOrm(name={self.name}, price={self.price})>"


class ToppingOrm(Base):
    __tablename__ = "toppings"

    topping_id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    pizzas: Mapped[List[PizzaOrm]] = relationship(
        "PizzaOrm",
        secondary=pizza_topping,
        back_populates="toppings",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<ToppingOrm(name={self.name}, price={self.price})>"
