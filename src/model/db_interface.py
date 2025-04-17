from typing import Optional
from abc import ABC, abstractmethod
from .entities import User, Order, Pizza, Topping, BasePizza


class Db(ABC):
    """Abstract interface for DB"""

    @abstractmethod
    def find_user(self, user_id: str) -> Optional[User]:
        """Find user by id"""
        pass

    def find_order(self, order_id: str) -> Order:
        """Find order by order id"""
        pass

    def find_pizza(self, pizza_id: str) -> Pizza:
        """Find pizza by pizza id"""
        pass

    def find_topping(self, topping_id: str):
        """Find topping by topping id"""
        pass

    def find_base_pizza(self, base_pizza_id: str) -> BasePizza:
        """Find base pizza by base pizza id"""
        pass

    def save_user(self, user: User):
        """Save user"""
        pass

    def save_order(self, order: Order):
        """Save order"""
        pass

    def save_topping(self, topping: Topping):
        """Save topping"""
        pass

    def save_base_pizza(self, base_pizza: BasePizza):
        """Save base pizza"""
        pass
