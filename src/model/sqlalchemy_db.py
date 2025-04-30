from typing import Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.dialects.postgresql import insert
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .entities import User, Order, Pizza, Topping, BasePizza
from .db_interface import Db
from .orm_models import UserOrm, OrderOrm, PizzaOrm, BasePizzaOrm, ToppingOrm
from db_engines import sync_session_factory, async_session_factory  # type: ignore


class SqlAlchemyDbSync(Db):

    def find_user(self, user_id: UUID) -> Optional[UserOrm]:
        with sync_session_factory() as session:
            return session.get(UserOrm, user_id)

    def find_order(self, order_id: UUID) -> Optional[OrderOrm]:
        with sync_session_factory() as session:
            stmt = select(OrderOrm).options(
                selectinload(OrderOrm.user),
                selectinload(OrderOrm.pizzas).selectinload(PizzaOrm.base_pizza),
                selectinload(OrderOrm.pizzas).selectinload(PizzaOrm.toppings),
            ).where(OrderOrm.order_id == order_id)
            res = session.execute(stmt)
            return res.scalar_one_or_none()

    def find_pizza(self, pizza_id: UUID) -> Optional[PizzaOrm]:
        with sync_session_factory() as session:
            stmt = select(PizzaOrm).options(
                selectinload(PizzaOrm.base_pizza),
                selectinload(PizzaOrm.toppings),
            ).where(PizzaOrm.pizza_id == pizza_id)
            res = session.execute(stmt)
            return res.scalar_one_or_none()

    def find_base_pizza(self, base_pizza_id: UUID) -> Optional[BasePizzaOrm]:
        with sync_session_factory() as session:
            return session.get(BasePizzaOrm, base_pizza_id)

    def find_topping(self, topping_id: UUID) -> Optional[ToppingOrm]:
        with sync_session_factory() as session:
            return session.get(ToppingOrm, topping_id)

    def save_user(self, user: UserOrm) -> None:
        with sync_session_factory() as session:
            print(">>> saving user with:", user.user_id, type(user.user_id))
            stmt = insert(UserOrm).values(
                user_id=user.user_id,
                name=user.name,
                phone_number=user.phone_number,
            ).on_conflict_do_update(
                index_elements=["user_id"],
                set_={
                    "name": user.name,
                    "phone_number": user.phone_number,
                }
            )
            session.execute(stmt)
            session.commit()

    def save_order(self, order: OrderOrm) -> None:
        with sync_session_factory() as session:
            print(">>> saving order with:", order.user_id, order.order_id)
            stmt = insert(OrderOrm).values(
                order_id=order.order_id,
                status=order.status.value,  # serialization of enum
                address=order.address,
                user_id=order.user_id,
            ).on_conflict_do_update(
                index_elements=["order_id"],
                set_={
                    "status": order.status,
                    "address": order.address,
                    "user_id": order.user_id,
                }
            )
            session.execute(stmt)
            session.commit()

    def save_topping(self, topping: ToppingOrm) -> None:
        with sync_session_factory() as session:
            stmt = insert(ToppingOrm).values(
                topping_id=topping.topping_id,
                name=topping.name,
                price=topping.price,
            ).on_conflict_do_update(
                index_elements=["topping_id"],
                set_={
                    "name": topping.name,
                    "price": topping.price,
                }
            )
            session.execute(stmt)
            session.commit()

    def save_base_pizza(self, base_pizza: BasePizzaOrm) -> None:
        with sync_session_factory() as session:
            stmt = insert(BasePizzaOrm).values(
                base_pizza_id=base_pizza.base_pizza_id,
                name=base_pizza.name,
                price=base_pizza.price,
            ).on_conflict_do_update(
                index_elements=["base_pizza_id"],
                set_={
                    "name": base_pizza.name,
                    "price": base_pizza.price,
                }
            )
            session.execute(stmt)
            session.commit()
