import uuid

from model.entities import Order, User, Pizza, OrderStatus
from model.in_mem_db import Db
from uuid import UUID


class PizzaService:
    def __init__(self, db: Db):
        self.db = db

    def create_order(self, user_id: UUID) -> Order:
        user = self.db.find_user(user_id)
        if not user:
            raise LookupError("User not found")
        order = Order(order_id=uuid.uuid4(), status=OrderStatus.NEW, user=user, pizzas=[], address="")
        self.db.save_order(order)
        return order

    def find_order(self, order_id: UUID) -> Order:
        return self.db.find_order(order_id)

    def add_user(self, name: str, phone_number: str) -> User:
        if not (phone_number.startswith("+7") and len(phone_number) == 12 and phone_number[1:].isdigit()):
            raise ValueError("Invalid phone number format. Must be +79XXXXXXXXX")
        user = User(user_id=uuid.uuid4(), name=name, phone_number=phone_number)
        self.db.save_user(user)
        return user

    def add_pizza(self, order_id: UUID, pizza: Pizza):
        order = self.db.find_order(order_id)
        if not order:
            raise LookupError("Order not found")
        if order.status != OrderStatus.NEW:
            raise PermissionError("Cannot add pizza to a non-new order")

        order.pizzas.append(pizza)
        self.db.save_order(order)

    def remove_pizza(self, order_id: UUID, pizza_id: UUID):
        order = self.db.find_order(order_id)
        if not order:
            raise LookupError("Order not found")
        if order.status != OrderStatus.NEW:
            raise PermissionError("Order is being prepared and can't be modified")
        order.pizzas = [p for p in order.pizzas if p.pizza_id != pizza_id]
        self.db.save_order(order)

    def update_address(self, order_id: UUID, new_address: str):
        order = self.db.find_order(order_id)
        if not order:
            raise LookupError("Order not found")
        if order.status != OrderStatus.NEW:
            raise PermissionError("Order is being prepared and the address can't be modified")

        order.address = new_address
        self.db.save_order(order)

    def calc_price(self, order_id: UUID) -> float:
        order = self.db.find_order(order_id)
        if not order:
            raise LookupError("Order not found")
        total_price = 0
        for pizza in order.pizzas:
            base_pizza = self.db.find_base_pizza(pizza.base_pizza_id)
            if not base_pizza:
                raise LookupError(f"Base pizza {pizza.base_pizza_id} not found")

            price = base_pizza.price
            for topping_id in pizza.topping_ids:
                topping = self.db.find_topping(topping_id)
                if not topping:
                    raise LookupError(f"Topping {topping_id} not found")

                price += topping.price
            total_price += price
        return total_price

    def on_payment_complete(self, order_id: UUID):
        order = self.db.find_order(order_id)
        if not order:
            raise LookupError("Order not found")
        if order.status != OrderStatus.ORDERED:
            raise PermissionError("Order can't be paid")

        order.status = OrderStatus.PREPARING
        self.db.save_order(order)

    def update_order_status(self, order_id: UUID, status: OrderStatus):
        # TODO: validate status
        # IMPORTANT: status can be updated only after validation
        order = self.db.find_order(order_id)
        if not order:
            raise LookupError("Order not found")
        if order.status == OrderStatus.COMPLETED:
            raise ValueError("Order has already been completed")
        # print(f"Current order status: {order.status}, Trying to set: {status}")

        status_order = {
            OrderStatus.NEW: [OrderStatus.ORDERED],
            OrderStatus.ORDERED: [OrderStatus.PREPARING],
            OrderStatus.PREPARING: [OrderStatus.READY],
            OrderStatus.READY: [OrderStatus.DELIVERING],
            OrderStatus.DELIVERING: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [OrderStatus.COMPLETED]
        }
        if status not in status_order.get(order.status, []):
            raise ValueError("We can't skip any status")

        order.status = status
        self.db.save_order(order)
        return True
