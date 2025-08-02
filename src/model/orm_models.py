from sqlalchemy import Column, Enum, ForeignKey, Table, select, String
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.dialects.postgresql import UUID as UUID_DB, ARRAY
from .entities import User, Order, Pizza, Topping, BasePizza
from enum import Enum as EnumPy
from typing import Annotated, List, Optional
# from model.entities import User, Order, Pizza, BasePizza, Topping
from uuid import UUID
from model.entities import OrderStatus


uuid_pk = Annotated[UUID, mapped_column(UUID_DB(as_uuid=True), primary_key=True)]


class Base(DeclarativeBase):
    pass


class UserOrm(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)

    def to_entity(self) -> User:
        return User(
            user_id=self.user_id,
            name=self.name,
            phone_number=self.phone_number
        )

    @classmethod
    def from_entity(cls, user: User) -> "UserOrm":
        return cls(
            user_id=user.user_id,
            name=user.name,
            phone_number=user.phone_number
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
        passive_deletes=True,
    )
    pizza_ids: Mapped[List[uuid_pk]] = mapped_column(ARRAY(String), nullable=False)

    @classmethod
    def from_entity(cls, order: Order, session: Session) -> "OrderOrm":
        user_orm = UserOrm.from_entity(order.user)

        pizza_ids = [pizza.pizza_id for pizza in order.pizzas]

        return cls(
            order_id=order.order_id,
            status=OrderStatus(order.status.value),
            user=user_orm,
            pizza_ids=pizza_ids,
            address=order.address,
        )

    def __repr__(self):
        return (f"<OrderOrm(order_id={self.order_id}, status={self.status}, user={self.user}, user_id={self.user_id},"
                f"pizzas={self.pizza_ids}, address={self.address})>")


class PizzaOrm(Base):
    __tablename__ = "pizzas"

    pizza_id: Mapped[uuid_pk]
    base_pizza_id: Mapped[UUID] = mapped_column(ForeignKey("base_pizzas.base_pizza_id", ondelete="CASCADE"))
    topping_ids: Mapped[list[uuid_pk]] = mapped_column(ARRAY(String), nullable=False)

    def to_entity(self) -> Pizza:
        return Pizza(
            pizza_id=self.pizza_id,
            base_pizza_id=self.base_pizza_id,
            topping_ids=self.topping_ids
        )

    @classmethod
    def from_entity(cls, pizza: Pizza, session: Session) -> "PizzaOrm":
        return cls(
            pizza_id=pizza.pizza_id,
            base_pizza_id=pizza.base_pizza_id,
            topping_ids=pizza.topping_ids
        )

    def __repr__(self):
        return f"<PizzaOrm(pizza_id={self.pizza_id})>"


class BasePizzaOrm(Base):
    __tablename__ = "base_pizzas"

    base_pizza_id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    def to_entity(self) -> BasePizza:
        return BasePizza(
            base_pizza_id=self.base_pizza_id,
            name=self.name,
            price=self.price
        )

    @classmethod
    def from_entity(cls, base_pizza: BasePizza) -> "BasePizzaOrm":
        return cls(
            base_pizza_id=base_pizza.base_pizza_id,
            name=base_pizza.name,
            price=base_pizza.price
        )

    def __repr__(self):
        return f"<BasePizzaOrm(name={self.name}, price={self.price})>"


class ToppingOrm(Base):
    __tablename__ = "toppings"

    topping_id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    def to_entity(self) -> Topping:
        return Topping(
            topping_id=self.topping_id,
            name=self.name,
            price=self.price
        )

    @classmethod
    def from_entity(cls, topping: Topping) -> "ToppingOrm":
        return cls(
            topping_id=topping.topping_id,
            name=topping.name,
            price=topping.price
        )

    def __repr__(self):
        return f"<ToppingOrm(name={self.name}, price={self.price})>"
