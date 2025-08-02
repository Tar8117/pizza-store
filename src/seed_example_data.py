from sqlalchemy.orm import Session
from uuid import uuid4
from db_engines import sync_engine, sync_session_factory
from model.orm_models import UserOrm, OrderOrm, PizzaOrm, BasePizzaOrm, ToppingOrm, OrderStatus


# Создаём сессию
# with Session(bind=sync_engine) as session: -> можно создать сессию и таким образом, а можно через фабрику сессий.
# Такой способ более "одноразовый"

if __name__ == '__main__':

    with sync_session_factory() as session:
        # Очистка предыдущих данных (если нужно)
        # session.execute(delete(UserOrm))
        # session.execute(delete(BasePizzaOrm))
        # session.execute(delete(ToppingOrm))

        # Примеры пользователей
        users = [
            UserOrm(user_id=uuid4(), name="Alice", phone_number="+79111111111"),
            UserOrm(user_id=uuid4(), name="Bob", phone_number="+79222222222")
        ]

        # Примеры базовых пицц
        base_pizzas = [
            BasePizzaOrm(base_pizza_id=uuid4(), name="Margherita", price=9.99),
            BasePizzaOrm(base_pizza_id=uuid4(), name="Pepperoni", price=11.99)
        ]

        # Примеры топпингов
        toppings = [
            ToppingOrm(topping_id=uuid4(), name="Cheese", price=1.5),
            ToppingOrm(topping_id=uuid4(), name="Mushrooms", price=2.0),
            ToppingOrm(topping_id=uuid4(), name="Olives", price=1.2)
        ]

        session.add_all(users + base_pizzas + toppings)
        session.commit()
        print("✅ База успешно заполнена тестовыми данными")
