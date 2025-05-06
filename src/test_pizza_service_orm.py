import pytest
import uuid
from .model.entities import OrderStatus, Pizza, BasePizza, Topping
from .model.in_mem_db import InMemDb
from .model.orm_models import BasePizzaOrm, ToppingOrm, UserOrm
from .model.sqlalchemy_db import SqlAlchemyDbSync
from .service.pizza_service import PizzaService


@pytest.fixture
def db():
    return SqlAlchemyDbSync()


@pytest.fixture
def service(db):
    return PizzaService(db)


@pytest.fixture
def user(service):
    return service.add_user(name="Oliver", phone_number="+79161234567")


# Фикстура создаёт базовую пиццу
@pytest.fixture
def base_pizza(db):
    base_pizza = BasePizza(base_pizza_id=uuid.uuid4(), name="Margherita", price=10.0)
    db.save_base_pizza(base_pizza)
    return base_pizza


# Фикстура создаёт топпинг
@pytest.fixture
def topping(db):
    topping = Topping(topping_id=uuid.uuid4(), name="Cheese", price=2.0)
    db.save_topping(topping)
    return topping


# Фикстура создаёт новый заказ
@pytest.fixture
def order(service, user):
    return service.create_order(user.user_id)


# Фикстура создаёт пиццу, используя базовую пиццу и топпинг
@pytest.fixture
def pizza(base_pizza, topping):
    return Pizza(pizza_id=uuid.uuid4(), base_pizza_id=base_pizza.base_pizza_id, topping_ids=[topping.topping_id])


# Фикстура с добавленной в заказ пиццей
@pytest.fixture
def order_with_pizza(service, order, base_pizza, topping):
    pizza = Pizza(pizza_id=uuid.uuid4(), base_pizza_id=base_pizza.base_pizza_id, topping_ids=[topping.topping_id])
    service.add_pizza(order.order_id, pizza)
    return order


# Тест создания пользователя
def test_add_user(service):
    user = service.add_user("Toni", "+79234567890")
    assert user.name == "Toni"
    assert user.phone_number == "+79234567890"


# Тест создания заказа
def test_create_order(service, user):
    order = service.create_order(user.user_id)
    assert order.user.user_id == user.user_id
    assert order.status == OrderStatus.NEW


# Тест добавления пиццы в заказ
def test_add_pizza(service, order, pizza):
    service.add_pizza(order.order_id, pizza)
    updated_order = service.db.find_order(order.order_id)
    assert len(updated_order.pizzas) == 1
    assert updated_order.pizzas[0].pizza_id == pizza.pizza_id


# Тест добавления и удаления пиццы из заказа
def test_remove_pizza(service, order, pizza):
    service.add_pizza(order.order_id, pizza)
    service.remove_pizza(order.order_id, pizza.pizza_id)
    updated_order = service.db.find_order(order.order_id)
    assert len(updated_order.pizzas) == 0


# Тест обновления адреса заказа
def test_update_address(service, order):
    service.update_address(order.order_id, "Moscow, Red square st")
    updated_order = service.db.find_order(order.order_id)
    assert updated_order.address == "Moscow, Red square st"


# Тест расчета стоимости заказа
def test_calc_price(service, order, pizza, base_pizza, topping):
    service.db.save_base_pizza(base_pizza)
    service.db.save_topping(topping)
    service.add_pizza(order.order_id, pizza)
    price = service.calc_price(order.order_id)
    assert price == 12.0  # 10 (base) + 2 (topping)


# Тест успешной оплаты заказа
def test_on_payment_complete(service, order):
    order.status = OrderStatus.ORDERED
    service.on_payment_complete(order.order_id)
    updated_order = service.db.find_order(order.order_id)
    assert updated_order.status == OrderStatus.PREPARING


# Тест обновления статуса заказа
def test_update_order_status(service, order):
    service.update_order_status(order.order_id, OrderStatus.ORDERED)
    service.update_order_status(order.order_id, OrderStatus.PREPARING)
    updated_order = service.db.find_order(order.order_id)
    assert updated_order.status == OrderStatus.PREPARING


# Тест на валидность номера телефона
def test_user_valid_phone(service):
    user = service.add_user("Tom", "+79234567890")
    assert user.name == "Tom"
    assert user.phone_number == "+79234567890"


# Тест на невалидный номер телефона
@pytest.mark.parametrize("invalid_phone", [
    "79123456789",
    "+7912345678",
    "+79abcdefghij",
    "+791234567890"
])
def test_add_user_invalid_phone(service, invalid_phone):
    with pytest.raises(ValueError, match="Invalid phone number format"):
        service.add_user("Tom", invalid_phone)


# Тест на пустой адрес после создания заказа и на обновление адреса в этом заказе
def test_create_order_with_address(service, user):
    order = service.create_order(user.user_id)
    assert order.address == ""

    service.update_address(order.order_id, "Moscow, Pizza Street, 52")
    assert order.address == "Moscow, Pizza Street, 52"


# Тест на правильную очередность переключение статусов заказа
def test_order_status_change(service, user):
    order = service.create_order(user.user_id)
    assert order.status == OrderStatus.NEW
    service.update_order_status(order.order_id, OrderStatus.ORDERED)
    assert order.status == OrderStatus.ORDERED
    service.update_order_status(order.order_id, OrderStatus.PREPARING)
    assert order.status == OrderStatus.PREPARING
    service.update_order_status(order.order_id, OrderStatus.READY)
    assert order.status == OrderStatus.READY

    with pytest.raises(ValueError, match="We can't skip any status"):
        service.update_order_status(order.order_id, OrderStatus.DELIVERED)  # Пропустили статус DELIVERING


# Тест на удаление пиццы (пицца уже добавлена в заказ через фикстуру)
def test_remove_pizza_from_order(service, order_with_pizza):
    order = order_with_pizza
    pizza_id = order.pizzas[0].pizza_id

    assert len(order.pizzas) == 1
    service.remove_pizza(order.order_id, pizza_id)
    assert len(order.pizzas) == 0


# Тест на удаление пиццы из пустого заказа
def test_remove_pizza_from_empty_order(service, user):
    order = service.create_order(user.user_id)
    service.remove_pizza(order.order_id, uuid.uuid4())
    assert len(order.pizzas) == 0


# Тест на полный цикл работы заказа
def test_pizza_service_happy_path(service, db, user, base_pizza, topping):
    # Сохраняем базовую пиццу и топпинг в БД
    db.save_base_pizza(base_pizza)
    db.save_topping(topping)

    # Создаём заказ
    order = service.create_order(user.user_id)

    # Добавляем пиццу в заказ
    pizza = Pizza(pizza_id=uuid.uuid4(), base_pizza_id=base_pizza.base_pizza_id, topping_ids=[topping.topping_id])
    service.add_pizza(order.order_id, pizza)

    # Обновляем адрес доставки
    service.update_address(order.order_id, "Russia, Moscow, Red Square, 1")

    # Проверяем статус заказа (должно быть NEW на данном этапе)
    assert order.status == OrderStatus.NEW

    # Проверяем корректность расчёта цены
    expected_price = base_pizza.price + topping.price
    assert service.calc_price(order.order_id) == expected_price

    # Устанавливаем и проверяем статус заказа (должно быть ORDERED на данном этапе, чтобы оплата прошла)
    service.update_order_status(order.order_id, OrderStatus.ORDERED)
    assert order.status == OrderStatus.ORDERED

    # Оплачиваем и подтверждаем оплату
    service.on_payment_complete(order.order_id)

    # После оплаты начинаем готовить и менять статусы
    # Мы не меняем статус на PREPARED, т.к. это происходит в методе on_payment_complete
    # Поэтому мы просто проверяем текущий статус (должно быть PREPARING на данном этапе)
    assert order.status == OrderStatus.PREPARING

    service.update_order_status(order.order_id, OrderStatus.READY)
    assert order.status == OrderStatus.READY

    service.update_order_status(order.order_id, OrderStatus.DELIVERING)
    assert order.status == OrderStatus.DELIVERING

    service.update_order_status(order.order_id, OrderStatus.DELIVERED)
    assert order.status == OrderStatus.DELIVERED

    service.update_order_status(order.order_id, OrderStatus.COMPLETED)
    assert order.status == OrderStatus.COMPLETED
