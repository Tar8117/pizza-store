from typing import Dict, Optional
from model.db_interface import Db
from model.entities import *
from uuid import UUID


class InMemDb(Db):
    def __init__(self):
        self.users: Dict[UUID, User] = dict()
        self.orders: Dict[UUID, Order] = dict()
        self.pizzas: Dict[UUID, Pizza] = dict()
        self.base_pizzas: Dict[UUID, BasePizza] = dict()
        self.toppings: Dict[UUID, Topping] = dict()

    def find_user(self, user_id: UUID) -> User:
        return self.users.get(user_id)

    def find_user_by_phone(self, phone_number: str) -> Optional[User]:
        for user in self.users.values():
            if user.phone_number == phone_number:
                return user
        return None

    def find_order(self, order_id: UUID) -> Order:
        return self.orders.get(order_id)

    def find_pizza(self, pizza_id: UUID) -> Pizza:
        return self.pizzas.get(pizza_id)

    def find_topping(self, topping_id: UUID) -> Topping:
        return self.toppings.get(topping_id)

    def find_base_pizza(self, base_pizza_id: UUID) -> BasePizza:
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

    def delete_pizza(self, pizza_id: UUID):
        self.pizzas.pop(pizza_id, None)
