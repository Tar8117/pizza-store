from service.pizza_service import PizzaService
from model.sqlalchemy_db import SqlAlchemyDbSync


def get_pizza_service() -> PizzaService:
    db = SqlAlchemyDbSync()
    return PizzaService(db=db)
