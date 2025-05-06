from sqlalchemy import Column, Enum, ForeignKey, Table, select, String
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.dialects.postgresql import UUID as UUID_DB, ARRAY
from .entities import User, Order, Pizza, Topping, BasePizza
from enum import Enum as EnumPy
from typing import Annotated, List
# from .entities import User, Order, Pizza, BasePizza, Topping
from uuid import UUID
from .entities import OrderStatus


uuid_pk = Annotated[UUID, mapped_column(UUID_DB(as_uuid=True), primary_key=True)]


class Base(DeclarativeBase):
    pass


# class OrderStatus(EnumPy):
#     NEW = "NEW"
#     ORDERED = "ORDERED"
#     PREPARING = "PREPARING"
#     READY = "READY"
#     DELIVERING = "DELIVERING"
#     DELIVERED = "DELIVERED"
#     COMPLETED = "COMPLETED"


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
        back_populates="orders",
        passive_deletes=True,
    )
    pizzas: Mapped[List["PizzaOrm"]] = relationship(
        "PizzaOrm",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    # pizzas: Mapped[str] = mapped_column(ARRAY(String))

    def to_entity(self) -> Order:
        return Order(
            order_id=self.order_id,
            status=OrderStatus(self.status.value),
            user=self.user.to_entity(),
            pizzas=[pizza.to_entity() for pizza in self.pizzas],
            address=self.address
        )

    @classmethod
    def from_entity(cls, order: Order, session: Session) -> "OrderOrm":
        user_orm = UserOrm.from_entity(order.user)

        pizzas = [PizzaOrm.from_entity(pizza, session) for pizza in order.pizzas]

        return cls(
            order_id=order.order_id,
            status=OrderStatus(order.status.value),
            user=user_orm,
            pizzas=pizzas,
            address=order.address,
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

    def to_entity(self) -> Pizza:
        return Pizza(
            pizza_id=self.pizza_id,
            base_pizza_id=self.base_pizza_id,
            topping_ids=[topping.topping_id for topping in self.toppings]
        )

    @classmethod
    def from_entity(cls, pizza: Pizza, session: Session) -> "PizzaOrm":
        base_pizza = session.execute(
            select(BasePizzaOrm).where(BasePizzaOrm.base_pizza_id == pizza.base_pizza_id)
        ).scalar_one_or_none()
        if not base_pizza:
            raise ValueError(f"BasePizza with id {pizza.base_pizza_id} not found")

        toppings = []
        if pizza.topping_ids:
            toppings = session.execute(
                select(ToppingOrm).where(ToppingOrm.topping_id.in_(pizza.topping_ids))
            ).scalars().all()

            missing_ids = set(pizza.topping_ids) - {t.topping_id for t in toppings}
            if missing_ids:
                raise ValueError(f"Toppings with ids {missing_ids} not found")

        return cls(
            pizza_id=pizza.pizza_id,
            base_pizza=base_pizza,
            toppings=toppings
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
    pizzas: Mapped[List[PizzaOrm]] = relationship(
        "PizzaOrm",
        secondary=pizza_topping,
        back_populates="toppings",
        passive_deletes=True,
    )

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
