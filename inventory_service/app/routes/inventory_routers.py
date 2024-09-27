from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from app.controllers.inventory_controllers import add_inventory, delete_inventory_by_id, get_inventory, get_inventory_id, update_inventory_by_id


inventory_router = APIRouter()

# Crud inventory

@inventory_router.post("/create_inventory")
async def add_inventories(added_inventoty: Annotated[dict, Depends(add_inventory)]):
    if added_inventoty:
        return added_inventoty
    raise HTTPException(status_code=404, detail="inventory is not added")
    


@inventory_router.get("/get_inventory")
def get_inventories(inventoty: Annotated[dict, Depends(get_inventory)]):
    if inventoty:
        return inventoty
    raise HTTPException(status_code=404, detail="inventory is not exist")


@inventory_router.get("/get_inventory_by_id/{inventory_id}")
def get_inventory_by_id(inventory: Annotated[dict, Depends(get_inventory_id)]):
    if inventory:
        return inventory
    raise HTTPException(status_code=404, detail="inventory is not exist")


@inventory_router.put("/update_inventory_by_id/{inventory_id}")
def update_inventory_id(updated_inventory: Annotated[dict, Depends(update_inventory_by_id)]):
    if updated_inventory:
        return updated_inventory
    raise HTTPException(status_code=404, detail="inventory is not updated")


@inventory_router.delete("/delete_inventory_by_id/{inventory_id}")
def delete_inventory_id(message: Annotated[str, Depends(delete_inventory_by_id)]):
    return message
