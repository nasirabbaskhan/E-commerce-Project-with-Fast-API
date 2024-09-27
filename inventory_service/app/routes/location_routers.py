from fastapi import Depends, APIRouter, HTTPException
from fastapi import Depends, APIRouter
from app.controllers.location_controllers import add_location, delete_location_by_id, get_location, get_location_id, update_location_by_id
from app.models.inventory_model import Location
from typing import Annotated




location_router = APIRouter()


# Crud location

@location_router.post("/create_location")
async def add_locations(added_location:Annotated[dict, Depends(add_location)]):
    if added_location:
        return added_location
    raise HTTPException(status_code=404, detail="inventory is not added")
   

@location_router.get("/get_location", response_model=list[Location])
def get_locations(location: Annotated[dict, Depends(get_location)]):
    if location:
        return location
    raise HTTPException(status_code=404, detail="location is not exist")


@location_router.get("/get_location_by_id/{location_id}")
def get_location_by_id( location: Annotated[dict, Depends(get_location_id)]):
    if location:
        return location
    raise HTTPException(status_code=404, detail="location is not exist")


@location_router.put("/location_update/{location_id}")
def update_location(updated_location: Annotated[dict, Depends(update_location_by_id)]):
    if updated_location:
        return updated_location
    raise HTTPException(status_code=404, detail="location is not updated")


@location_router.delete("/delete_location_by_id/{location_id}")
def delete_location_id(message: Annotated[str, Depends(delete_location_by_id)]):
    return message