from typing import Dict, Optional
from abc import ABC, abstractmethod

from .entities import *


# Interface for db
class Db(ABC):
    @abstractmethod
    def find_user(self, user_id: str) -> Optional[User]:
        pass

    def find_order(self, order_id: str) -> Order:
        pass

    def find_pizza(self, pizza_id: str) -> Pizza:
        pass

    def find_topping(self, topping_id: str):
        pass

    def find_base_pizza(self, base_pizza_id: str) -> BasePizza:
        pass

    # def add_user(self, user: User):
    #     pass

    def save_user(self, user: User):
        pass

    def save_order(self, order: Order):
        pass

    def save_topping(self, topping: Topping):
        pass

    def save_base_pizza(self, base_pizza: BasePizza):
        pass


class InMemDb(Db):
    def __init__(self):
        self.users: Dict[str, User] = dict()
        self.orders: Dict[str, Order] = dict()
        self.pizzas: Dict[str, Pizza] = dict()
        self.base_pizzas: Dict[str, BasePizza] = dict()
        self.toppings: Dict[str, Topping] = dict()

    # Вопросы: Почему id не int, а str?
    def find_user(self, user_id: str) -> User:
        return self.users.get(user_id)

    def find_order(self, order_id: str) -> Order:
        return self.orders.get(order_id)

    def find_pizza(self, pizza_id: str) -> Pizza:
        return self.pizzas.get(pizza_id)

    def find_topping(self, topping_id: str) -> Topping:
        return self.toppings.get(topping_id)

    def find_base_pizza(self, base_pizza_id: str) -> BasePizza:
        return self.base_pizzas.get(base_pizza_id)

    def save_user(self, user: User):
        self.users[user.user_id] = user

    def save_order(self, order: Order):
        self.orders[order.order_id] = order

    def save_pizza(self, pizza: Pizza):
        self.pizzas[pizza.pizza_id] = pizza

    def save_topping(self, topping: Topping):
        self.toppings[topping.topping_id] = topping

    def save_base_pizza(self, base_pizza: BasePizza):
        self.base_pizzas[base_pizza.base_pizza_id] = base_pizza
