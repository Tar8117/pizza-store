from db_engines import sync_engine
from model.orm_models import Base
from uuid import UUID, uuid4
from db_engines import sync_session_factory
from model.sqlalchemy_db import SqlAlchemyDbSync
from model.orm_models import UserOrm, OrderOrm, PizzaOrm, BasePizzaOrm, ToppingOrm, OrderStatus
from sqlalchemy import delete, select, text

# Создать таблицы
Base.metadata.create_all(bind=sync_engine)
print("✅ Таблицы созданы!")

# Удалить таблицы
# Base.metadata.drop_all(bind=sync_engine)
# print("🗑️ Таблицы удалены!")

# Удалить таблицы
# with sync_engine.connect() as conn:
#     conn.execute(text("DROP SCHEMA public CASCADE"))
#     print("🗑️ Все таблицы удалены с CASCADE!")

# Разные запросы.
# Поменять номер телефона пользователя:
# with sync_session_factory() as session:
#     user = session.query(UserOrm).filter_by(user_id=UUID("bfa57f34-b980-40ad-a1f6-7adaff7c235b")).first()
#     user.phone_number = "+79295264098"
#     session.commit()

# Поменять имя пользователя:
# with sync_session_factory() as session:
#     user = session.query(UserOrm).filter_by(user_id=UUID("bfa57f34-b980-40ad-a1f6-7adaff7c235b")).first()
#     user.name = "Bob_edited"
#     session.commit()

# Поменять имя пользователя новый синтаксис:
# with sync_session_factory() as session:
#     stmt = select(UserOrm).where(UserOrm.user_id == UUID("bfa57f34-b980-40ad-a1f6-7adaff7c235b"))
#     user = session.scalars(stmt).first()
#     user.name = "Bob_edited_2"
#     session.commit()

# Запрос пицц
# with sync_session_factory() as session:
#     stmt = session.query(BasePizzaOrm).all()
#     for pizza in stmt:
#         print(pizza.name)
#
# db = SqlAlchemyDbSync()
# with sync_session_factory() as test_find_user:
#     stmt = db.find_user(UUID("3bd80fcf-7f4b-4687-8fe4-c8bc96e686d4"))
#     stmt2 = db.find_user(UUID("5bb07e9d-ef81-44e3-995e-5de3d3bfc1ba"))
#     print(stmt, stmt2)
#
# # with Session(bind=sync_engine) as session:
# with sync_session_factory() as test_find_order:
#     stmt = db.find_order(UUID("03349ae3-9006-4d8a-b760-2b688ed8570e"))
#     stmt2 = db.find_order(UUID("dc799973-a27a-48b6-a5e9-e331b4313ce0"))
#     print(stmt, stmt2)
#
# with sync_session_factory() as test_find_pizza:
#     stmt = db.find_pizza(UUID("d0e4e3a6-f722-4854-aaf1-7015ecd63560"))
#     stmt2 = db.find_pizza(UUID("ddc54a14-94d4-4495-a44e-6014418be0af"))
#     print(stmt, stmt2)
#
# with sync_session_factory() as test_find_base_pizza:
#     stmt = db.find_base_pizza(UUID("c9e1f2ac-6f81-42ba-9398-60072116ca81"))
#     stmt2 = db.find_base_pizza(UUID("0d3ef25a-bcc8-4b4e-b972-aaa956a30c23"))
#     print(stmt, stmt2)
#
# with sync_session_factory() as test_find_topping:
#     stmt = db.find_topping(UUID("057b66f7-5954-43c2-8f42-42372031ab03"))
#     stmt2 = db.find_topping(UUID("e56a5780-ffc1-4e95-bb2d-0ff808bfc13e"))
#     print(stmt, stmt2)

# --- TEST SAVE USER ---
# with sync_session_factory() as test_save_user:
#     user_id = uuid4()
#     user = UserOrm(user_id=user_id, name="Bob", phone_number="+79164546677")
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
# with sync_session_factory() as session:
#     # создаём заказ
#     order_id = uuid4()
#     order = OrderOrm(
#         order_id=order_id,
#         status=OrderStatus.NEW,
#         address="First Address",
#         user_id=UUID("b86343b4-b8f9-49b1-a7d6-b02bc68e15c2"),
#     )
#     db.save_order(order)
#
#     # проверяем
#     saved_order = db.find_order(order_id)
#     print("First save:", saved_order)
#
#     # обновляем
#     updated_order = OrderOrm(
#         order_id=order_id,
#         status=OrderStatus.READY,
#         address="Updated Address",
#         user_id=UUID("b86343b4-b8f9-49b1-a7d6-b02bc68e15c2"),
#     )
#     db.save_order(updated_order)
#
#     updated = db.find_order(order_id)
#     print("After update:", updated)

# Поменять статус заказа:
# with sync_session_factory() as session:
#     stmt = select(OrderOrm).where(OrderOrm.order_id == UUID("e150fdb7-df3d-4d19-a256-61bfebc6a06a"))
#     order = session.scalars(stmt).first()
#     order.status = OrderStatus.DELIVERING
#     session.commit()

# --- TEST SAVE TOPPING ---
# with sync_session_factory() as test_save_topping:
#     topping_id = uuid4()
#     topping = ToppingOrm(topping_id=topping_id, name="Ricotta", price=1.5)
#     db.save_topping(topping)
#
#     saved_topping = db.find_topping(topping_id)
#     print(saved_topping)
#
#     # обновляем
#     topping.price = 2.0
#     db.save_topping(topping)
#
#     updated_topping = db.find_topping(topping_id)
#     print(updated_topping)

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
# with sync_session_factory() as del_user:
#     stmt = delete(UserOrm).where(UserOrm.user_id == UUID("b86343b4-b8f9-49b1-a7d6-b02bc68e15c2"))
#     del_user.execute(stmt)
#     del_user.commit()

# Удалить топпинг по пк
# with sync_session_factory() as del_topping:
#     stmt = delete(ToppingOrm).where(ToppingOrm.topping_id == UUID("64e59299-0af9-4ea3-864e-c88474e6a884"))
#     del_topping.execute(stmt)
#     del_topping.commit()

# Удалить заказ по пк
# with sync_session_factory() as del_order:
#     stmt = delete(OrderOrm).where(OrderOrm.order_id == UUID("cb2c03aa-2f1d-4823-a4db-4448e01b80bd"))
#     del_order.execute(stmt)
#     del_order.commit()
