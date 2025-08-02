from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from service.pizza_service import PizzaService
from model.entities import Pizza
from api.dependencies import get_pizza_service
from api.schemas import *


router = APIRouter()


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, service: PizzaService = Depends(get_pizza_service)):
    try:
        return service.add_user(name=user.name, phone_number=user.phone_number)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/orders/{user_id}", response_model=OrderOut)
def create_order(user_id: UUID, service: PizzaService = Depends(get_pizza_service)):
    try:
        return service.create_order(user_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: UUID, service: PizzaService = Depends(get_pizza_service)):
    order = service.find_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/orders/{order_id}/pizza", status_code=204)
def add_pizza(order_id: UUID, pizza: PizzaIn, service: PizzaService = Depends(get_pizza_service)):
    try:
        service.add_pizza(order_id, pizza)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/orders/{order_id}/pizza/{pizza_id}", status_code=204)
def remove_pizza(order_id: UUID, pizza_id: UUID, service: PizzaService = Depends(get_pizza_service)):
    try:
        service.remove_pizza(order_id, pizza_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.patch("/orders/{order_id}/address", status_code=204)
def update_address(order_id: UUID, data: AddressUpdate, service: PizzaService = Depends(get_pizza_service)):
    try:
        service.update_address(order_id, data.address)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/orders/{order_id}/price", response_model=float)
def calc_price(order_id: UUID, service: PizzaService = Depends(get_pizza_service)):
    try:
        return service.calc_price(order_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/orders/{order_id}/payment", status_code=204)
def payment_complete(order_id: UUID, service: PizzaService = Depends(get_pizza_service)):
    try:
        service.on_payment_complete(order_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.patch("/orders/{order_id}/status", status_code=200)
def update_status(order_id: UUID, data: OrderStatusUpdate, service: PizzaService = Depends(get_pizza_service)):
    try:
        service.update_order_status(order_id, data.status)
        return {"status": "updated"}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))