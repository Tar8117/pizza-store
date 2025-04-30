from typing import Optional
from abc import ABC, abstractmethod
from .entities import User, Order, Pizza, Topping, BasePizza


class Db(ABC):
    """Abstract interface for DB"""

    @abstractmethod
    def find_user(self, user_id: str) -> Optional[User]:
        """Find user by id"""
        pass

    @abstractmethod
    def find_order(self, order_id: str) -> Optional[Order]:
        """Find order by order id"""
        pass

    @abstractmethod
    def find_pizza(self, pizza_id: str) -> Optional[Pizza]:
        """Find pizza by pizza id"""
        pass

    @abstractmethod
    def find_topping(self, topping_id: str) -> Optional[Topping]:
        """Find topping by topping id"""
        pass

    @abstractmethod
    def find_base_pizza(self, base_pizza_id: str) -> Optional[BasePizza]:
        """Find base pizza by base pizza id"""
        pass

    @abstractmethod
    def save_user(self, user: User) -> None:
        """Save user"""
        pass

    @abstractmethod
    def save_order(self, order: Order) -> None:
        """Save order"""
        pass

    @abstractmethod
    def save_topping(self, topping: Topping) -> None:
        """Save topping"""
        pass

    @abstractmethod
    def save_base_pizza(self, base_pizza: BasePizza) -> None:
        """Save base pizza"""
        pass
