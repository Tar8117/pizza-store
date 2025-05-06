from typing import Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.dialects.postgresql import insert
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .entities import User, Order, Pizza, Topping, BasePizza
from .db_interface import Db
from .orm_models import UserOrm, OrderOrm, PizzaOrm, BasePizzaOrm, ToppingOrm
from ..db_engines import sync_session_factory, async_session_factory  # type: ignore


class SqlAlchemyDbSync(Db):

    def find_user(self, user_id: UUID) -> Optional[User]:
        with sync_session_factory() as session:
            # return session.get(UserOrm, user_id)
            orm_user = session.get(UserOrm, user_id)
            return orm_user.to_entity() if orm_user else None

    def find_order(self, order_id: UUID) -> Optional[Order]:
        with sync_session_factory() as session:
            stmt = select(OrderOrm).options(
                selectinload(OrderOrm.user),
                selectinload(OrderOrm.pizzas).selectinload(PizzaOrm.base_pizza),
                selectinload(OrderOrm.pizzas).selectinload(PizzaOrm.toppings),
            ).where(OrderOrm.order_id == order_id)
            res = session.execute(stmt)
            # return res.scalar_one_or_none()
            orm_order = res.scalar_one_or_none()
            return orm_order.to_entity() if orm_order else None

    def find_pizza(self, pizza_id: UUID) -> Optional[Pizza]:
        with sync_session_factory() as session:
            stmt = select(PizzaOrm).options(
                selectinload(PizzaOrm.base_pizza),
                selectinload(PizzaOrm.toppings),
            ).where(PizzaOrm.pizza_id == pizza_id)
            res = session.execute(stmt)
            # return res.scalar_one_or_none()
            orm_pizza = res.scalar_one_or_none()
            return orm_pizza.to_entity() if orm_pizza else None

    def find_base_pizza(self, base_pizza_id: UUID) -> Optional[BasePizza]:
        with sync_session_factory() as session:
            # return session.get(BasePizzaOrm, base_pizza_id)
            orm_base_pizza = session.get(BasePizzaOrm, base_pizza_id)
            return orm_base_pizza.to_entity() if orm_base_pizza else None

    def find_topping(self, topping_id: UUID) -> Optional[Topping]:
        with sync_session_factory() as session:
            # return session.get(ToppingOrm, topping_id)
            orm_topping = session.get(ToppingOrm, topping_id)
            return orm_topping.to_entity() if orm_topping else None

    def save_user(self, user: User) -> None:
        with sync_session_factory() as session:
            orm_user = UserOrm.from_entity(user)
            # print(">>> saving user with:", user.user_id, type(user.user_id))
            stmt = insert(UserOrm).values(
                user_id=orm_user.user_id,
                name=orm_user.name,
                phone_number=orm_user.phone_number,
            ).on_conflict_do_update(
                index_elements=["user_id"],
                set_={
                    "name": orm_user.name,
                    "phone_number": orm_user.phone_number,
                }
            )
            session.execute(stmt)
            session.commit()

    def save_order(self, order: Order) -> None:
        with sync_session_factory() as session:
            orm_order = OrderOrm.from_entity(order, session)
            # print(">>> saving order with:", order.user_id, order.order_id)
            stmt = insert(OrderOrm).values(
                order_id=orm_order.order_id,
                status=orm_order.status.value,  # serialization of enum
                address=orm_order.address,
                user_id=orm_order.user.user_id,
            ).on_conflict_do_update(
                index_elements=["order_id"],
                set_={
                    "status": orm_order.status,
                    "address": orm_order.address,
                    "user_id": orm_order.user.user_id,
                }
            )
            session.execute(stmt)
            session.commit()

    def save_topping(self, topping: Topping) -> None:
        with sync_session_factory() as session:
            orm_topping = ToppingOrm.from_entity(topping)
            stmt = insert(ToppingOrm).values(
                topping_id=orm_topping.topping_id,
                name=orm_topping.name,
                price=orm_topping.price,
            ).on_conflict_do_update(
                index_elements=["topping_id"],
                set_={
                    "name": orm_topping.name,
                    "price": orm_topping.price,
                }
            )
            session.execute(stmt)
            session.commit()

    def save_base_pizza(self, base_pizza: BasePizza) -> None:
        with sync_session_factory() as session:
            orm_base_pizza = BasePizzaOrm.from_entity(base_pizza)
            stmt = insert(BasePizzaOrm).values(
                base_pizza_id=orm_base_pizza.base_pizza_id,
                name=orm_base_pizza.name,
                price=orm_base_pizza.price,
            ).on_conflict_do_update(
                index_elements=["base_pizza_id"],
                set_={
                    "name": orm_base_pizza.name,
                    "price": orm_base_pizza.price,
                }
            )
            session.execute(stmt)
            session.commit()
