from db_engines import sync_engine
from model.orm_models import Base
from uuid import UUID, uuid4
from db_engines import sync_session_factory
from model.sqlalchemy_db import SqlAlchemyDbSync
from model.orm_models import UserOrm, OrderOrm, PizzaOrm, BasePizzaOrm, ToppingOrm, OrderStatus
from sqlalchemy import delete


# Создать таблицы
# Base.metadata.create_all(bind=sync_engine)
# print("✅ Таблицы созданы!")

# Удалить таблицы
# Base.metadata.drop_all(bind=sync_engine)
# print("🗑️ Таблицы удалены!")

# Разные запросы.
# Поменять номер телефона пользователя:
# with sync_session_factory() as session:
#     user = session.query(UserOrm).filter_by(name="Bob").first()
#     user.phone_number = "+79254564455"
#     session.commit()


# Запрос пицц
# with sync_session_factory() as session:
#     stmt = session.query(BasePizzaOrm).all()
#     for pizza in stmt:
#         print(pizza.name)
#
db = SqlAlchemyDbSync()
# with sync_session_factory() as test_find_user:
#     stmt = db.find_user(UUID("51d0c103-8b2f-4845-842e-c280979ac3eb"))
#     stmt2 = db.find_user(UUID("5bb07e9d-ef81-44e3-995e-5de3d3bfc1ba"))
#     print(stmt, stmt2)
#
# # with Session(bind=sync_engine) as session:
# with sync_session_factory() as test_find_order:
#     stmt = db.find_order(UUID("51d0c103-8b2f-4845-842e-c280979ac3eb"))
#     stmt2 = db.find_order(UUID("dc799973-a27a-48b6-a5e9-e331b4313ce0"))
#     print(stmt, stmt2)
#
# with sync_session_factory() as test_find_pizza:
#     stmt = db.find_pizza(UUID("51d0c103-8b2f-4845-842e-c280979ac3eb"))
#     stmt2 = db.find_pizza(UUID("ddc54a14-94d4-4495-a44e-6014418be0af"))
#     print(stmt, stmt2)
#
# with sync_session_factory() as test_find_base_pizza:
#     stmt = db.find_base_pizza(UUID("51d0c103-8b2f-4845-842e-c280979ac3eb"))
#     stmt2 = db.find_base_pizza(UUID("0d3ef25a-bcc8-4b4e-b972-aaa956a30c23"))
#     print(stmt, stmt2)
#
# with sync_session_factory() as test_find_topping:
#     stmt = db.find_topping(UUID("51d0c103-8b2f-4845-842e-c280979ac3eb"))
#     stmt2 = db.find_topping(UUID("e56a5780-ffc1-4e95-bb2d-0ff808bfc13e"))
#     print(stmt, stmt2)

# --- TEST SAVE USER ---
# with sync_session_factory() as test_save_user:
#     user_id = uuid4()
#     user = UserOrm(user_id=user_id, name="Jimmy", phone_number="+79164546677")
#     db.save_user(user)
#
#     saved_user = db.find_user(user_id)
#     print(saved_user)
#
#     # теперь обновляем
#     user = UserOrm(user_id=user_id, name="Jimmy_UPDATED_NEW", phone_number="+79164546677")
#     db.save_user(user)
#
#     updated_user = db.find_user(user_id)
#     print(updated_user)

# --- TEST SAVE ORDER ---
with sync_session_factory() as session:
    # создаём заказ
    order_id = uuid4()
    order = OrderOrm(
        order_id=order_id,
        status=OrderStatus.NEW,
        address="First Address",
        user_id=UUID("3e349c80-6ef7-4057-b185-6608e8b1d5b4"),
    )
    db.save_order(order)

    # проверяем
    saved_order = db.find_order(order_id)
    print("First save:", saved_order)

    # обновляем
    updated_order = OrderOrm(
        order_id=order_id,
        status=OrderStatus.READY,
        address="Updated Address",
        user_id=UUID("3e349c80-6ef7-4057-b185-6608e8b1d5b4"),
    )
    db.save_order(updated_order)

    updated = db.find_order(order_id)
    print("After update:", updated)

# --- TEST SAVE TOPPING ---
with sync_session_factory() as test_save_topping:
    topping_id = uuid4()
    topping = ToppingOrm(topping_id=topping_id, name="Ricotta", price=1.5)
    db.save_topping(topping)

    saved_topping = db.find_topping(topping_id)
    print(saved_topping)

    # обновляем
    topping.price = 2.0
    db.save_topping(topping)

    updated_topping = db.find_topping(topping_id)
    print(updated_topping)

# --- TEST SAVE BASE PIZZA ---
# with sync_session_factory() as test_save_base_pizza:
#     base_pizza_id = uuid4()
#     base_pizza = BasePizzaOrm(base_pizza_id=base_pizza_id, name="Diablo", price=5.0)
#     db.save_base_pizza(base_pizza)
#
#     saved_base_pizza = db.find_base_pizza(base_pizza_id)
#     print(saved_base_pizza)
#
#     # обновляем
#     base_pizza.price = 6.0
#     db.save_base_pizza(base_pizza)
#
#     updated_base_pizza = db.find_base_pizza(base_pizza_id)
#     print(updated_base_pizza)

# Удалить юзера по пк
# with sync_session_factory() as session:
#     stmt = delete(UserOrm).where(UserOrm.user_id == UUID("49603e1f-7fdb-4e34-b2cb-1df01610da35"))
#     session.execute(stmt)
#     session.commit()

# Удалить топпинг по пк
# with sync_session_factory() as del_topping:
#     stmt = delete(ToppingOrm).where(ToppingOrm.topping_id == UUID("5e9fef96-40cf-4939-ad73-f381a9998421"))
#     del_topping.execute(stmt)
#     del_topping.commit()

# Удалить заказ по пк
# with sync_session_factory() as del_order:
#     stmt = delete(OrderOrm).where(OrderOrm.order_id == UUID("6f3fb2ff-f631-4716-8346-b0fba10eb979"))
#     del_order.execute(stmt)
#     del_order.commit()
