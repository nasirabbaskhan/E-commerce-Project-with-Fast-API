
from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime
from typing import Annotated

from app.controllers.orders_controllers import create_order, delete_order_id, get_order_id, get_orders, update_order


order_router = APIRouter()

# Crud Order

@order_router.post("/order_add")
async def add_order(added_order:Annotated[dict, Depends(create_order)]):
    if added_order:
        return added_order
    raise HTTPException(status_code=404, detail="order is not added")


@order_router.get("/orders")
def get_all_orders(order: Annotated[dict, Depends(get_orders)]):
    if order:
        return order
    raise HTTPException(status_code=404, detail="oredr is not exist")


@order_router.get("/order/{order_id}")
def get_order_by_id(order: Annotated[dict, Depends(get_order_id)]):
    if order:
        return order
    raise HTTPException(status_code=404, detail="order is not exist")





@order_router.put("/order_update/{order_id}")
def update_order_by_id(updated_order: Annotated[dict, Depends(update_order)]):
    if updated_order:
        return updated_order
    raise HTTPException(status_code=404, detail="order is not updated")


@order_router.delete("/order_delete/{order_id}")
def delete_order_by_id(message: Annotated[str, Depends(delete_order_id)]):
    if message:
        return message
    raise HTTPException(status_code=404, detail="order is not deleted")
