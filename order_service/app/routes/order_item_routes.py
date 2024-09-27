
from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated

from app.controllers.order_item_controllers import create_order_item, delete_order_item_id, get_order_item_id, get_order_items, update_order_item

orderitem_router = APIRouter()



# Crud OrderItems

@orderitem_router.post("/order_item_add")
async def add_order_item(added_order_item:Annotated[dict, Depends(create_order_item)]):
    if added_order_item:
        return added_order_item
    raise HTTPException(status_code=404, detail="order_item is not added")


@orderitem_router.get("/order_items")
def get_all_order_items(order_item: Annotated[dict, Depends(get_order_items)]):
    if order_item:
        return order_item
    raise HTTPException(status_code=404, detail="order_item is not exist")


@orderitem_router.get("/order_item/{order_item_id}")
def get_order_item_by_id(order_item: Annotated[dict, Depends(get_order_item_id)]):
    if order_item:
        return order_item
    raise HTTPException(status_code=404, detail="order_item is not exist")





@orderitem_router.put("/order_item_update/{order_item_id}")
def update_order_item_by_id(updated_order_item: Annotated[dict, Depends(update_order_item)]):
    if updated_order_item:
        return updated_order_item
    raise HTTPException(status_code=404, detail="order_item is not updated")


@orderitem_router.delete("/order_item_delete/{order_item_id}")
def delete_order_item_by_id(message: Annotated[str, Depends(delete_order_item_id)]):
    if message:
        return message
    raise HTTPException(status_code=404, detail="order_item is not deleted")
