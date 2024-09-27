
from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated

from app.controllers.shipment_controllers import create_shipment, delete_shipment_id, get_shipment_id, get_shipments, update_shipment







shipment_router = APIRouter()


# Crud Shipment

@shipment_router.post("/shipment_add")
async def add_shipment(added_shipment: Annotated[dict, Depends(create_shipment)]):
    if added_shipment:
        return added_shipment
    raise HTTPException(status_code=404, detail="shipment is not added")
    
        

@shipment_router.get("/shipments")
def get_all_shipments(shipment: Annotated[dict, Depends(get_shipments)]):
    if shipment:
        return shipment
    raise HTTPException(status_code=404, detail="shipment is not exist")


@shipment_router.get("/shipment/{shipment_id}")
def get_shipment_by_id(shipment: Annotated[dict, Depends(get_shipment_id)]):
    if shipment:
        return shipment
    raise HTTPException(status_code=404, detail="shipment is not exist")





@shipment_router.put("/shipment_update/{shipment_id}")
def update_shipment_by_id(updated_shipment: Annotated[dict, Depends(update_shipment)]):
    if updated_shipment:
        return updated_shipment
    raise HTTPException(status_code=404, detail="shipment is not updated")


@shipment_router.delete("/shipment_delete/{shipment_id}")
def delete_shipment_by_id(message: Annotated[str, Depends(delete_shipment_id)]):
    if message:
        return message
    raise HTTPException(status_code=404, detail="notification is not deleted")
