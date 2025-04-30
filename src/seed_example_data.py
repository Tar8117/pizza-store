from sqlalchemy.orm import Session
from uuid import uuid4
from db_engines import sync_engine, sync_session_factory
from model.orm_models import UserOrm, OrderOrm, PizzaOrm, BasePizzaOrm, ToppingOrm, OrderStatus


# Создаём сессию
# with Session(bind=sync_engine) as session: -> можно создать сессию и таким образом, а можно через фабрику сессий.
# Такой способ более "одноразовый"

with sync_session_factory() as session:
    # 1. Создаём базовые пиццы и топпинги
    base_pepperoni = BasePizzaOrm(base_pizza_id=uuid4(), name="Pepperoni", price=8.0)
    base_margherita = BasePizzaOrm(base_pizza_id=uuid4(), name="Margherita", price=6.5)

    topping_cheese = ToppingOrm(topping_id=uuid4(), name="Extra Cheese", price=1.5)
    topping_olives = ToppingOrm(topping_id=uuid4(), name="Olives", price=1.0)
    topping_peppers = ToppingOrm(topping_id=uuid4(), name="Peppers", price=0.8)

    # 2. Создаём пользователя
    user = UserOrm(user_id=uuid4(), name="Alice", phone_number="+79261234567")
    user2 = UserOrm(user_id=uuid4(), name="Bob", phone_number="987654321")

    # 3. Создаём заказ
    order = OrderOrm(order_id=uuid4(), status=OrderStatus.NEW, address="123 Main St", user=user)
    order2 = OrderOrm(order_id=uuid4(), status=OrderStatus.NEW, address="456 Broadway", user=user2)

    # 4. Создаём пиццу в заказе
    pizza = PizzaOrm(
        pizza_id=uuid4(),
        order=order,
        base_pizza=base_pepperoni,
        toppings=[topping_cheese, topping_olives],
    )

    pizza2 = PizzaOrm(
        pizza_id=uuid4(),
        order=order2,
        base_pizza=base_margherita,
        toppings=[topping_olives, topping_peppers],
    )

    # 5. Добавляем всё в сессию
    session.add_all([
        base_pepperoni, base_margherita, topping_cheese, topping_olives, topping_peppers, user, user2, order, order2,
        pizza, pizza2
    ])
    session.commit()

    print("✅ Примерные данные добавлены!")
