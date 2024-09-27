from typing import Annotated
from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import Depends, APIRouter, HTTPException

from app.controllers.notification_controllers import add_notification, delete_notifications, get_notification_id, get_notifications, update_notifications


notification_router = APIRouter()


# Crud Notification

@notification_router.post("/add_notification")
async def create_notification(added_notification:Annotated[dict, Depends(add_notification)]):
    if added_notification:
        return added_notification
    raise HTTPException(status_code=404, detail="Notification is not added")

        
        

@notification_router.get("/notification")
def get_notification(notification: Annotated[dict, Depends(get_notifications)]):
    if notification:
        return notification
    raise HTTPException(status_code=404, detail="notification is not exist")


@notification_router.get("/notification/{notification_id}")
def get_notification_by_id(notification: Annotated[dict, Depends(get_notification_id)]):
    if notification:
        return notification
    raise HTTPException(status_code=404, detail="notification is not exist")





@notification_router.put("/update_notification/{notification_id}")
def update_notification(updated_notofication: Annotated[dict, Depends(update_notifications)],):
    if updated_notofication:
        return updated_notofication
    raise HTTPException(status_code=404, detail="notification is not updated")



@notification_router.delete("/delete_notification/{notification_id}")
def delete_notification(message: Annotated[str, Depends(delete_notifications)]):
    if message:
        return message
    raise HTTPException(status_code=404, detail="notification is not deleted")
