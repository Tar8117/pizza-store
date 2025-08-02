import pytest
from model.orm_models import Base
from db_engines import sync_engine


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Создаёт таблицы перед запуском всех тестов и удаляет их после."""
    print("\n📦 Создание таблиц для тестов")
    Base.metadata.create_all(bind=sync_engine)
    yield
    print("\n🧹 Удаление таблиц после тестов")
    Base.metadata.drop_all(bind=sync_engine)


# @pytest.fixture(autouse=True)
# def clean_data():
#     """Очищает данные в таблицах перед каждым тестом."""
#     from sqlalchemy import text
#     with sync_engine.connect() as conn:
#         conn.execute(text("TRUNCATE users, orders, pizzas, base_pizzas, toppings RESTART IDENTITY CASCADE"))
#         conn.commit()
