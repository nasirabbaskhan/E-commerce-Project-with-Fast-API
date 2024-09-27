from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.db.db_connectivity import get_session
from app.models.notification_models import Notification, NotificationAdd, NotificationUpdate
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.producers import get_kafka_producer
from app import notification_pb2
from google.protobuf.json_format import MessageToDict



# crud notification

async def add_notification(notification_add:NotificationAdd, session: Annotated[Session, Depends(get_session)],
                           producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    try:
        
        notification_proto=notification_pb2.Notification_Proto(user_id=notification_add.user_id, order_id=notification_add.order_id, message=notification_add.message, read=notification_add.read)
        print(f"notification_proto: {notification_proto}")
        serialized_notification=notification_proto.SerializeToString()
        print(f"serialized_notification: {serialized_notification}")

        try:
            await producer.send_and_wait("notification", serialized_notification)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")

        # Convert Protobuf object to a dictionary
        user_dict = MessageToDict(notification_proto)

        return user_dict
        
        
        # db_notification = Notification(
        #     user_id=notification_add.user_id,
        #     order_id=notification_add.order_id,
        #     message=notification_add.message,
        #     read=notification_add.read
            
        # )
        # session.add(db_notification)
        # session.commit()
        # session.refresh(db_notification)
        # return db_notification
    except Exception as e:
        print(e)


def get_notifications(session: Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.exec(select(Notification)).all()
        return get_data
    except Exception as e:
        print(e)


def get_notification_id(notification_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Notification, notification_id)
        return get_data
    except Exception as e:
        print(e)




def update_notifications(notification_id: int, notification_update: NotificationUpdate, session: Annotated[Session, Depends(get_session)]):
    try:
        db_notification = session.get(Notification, notification_id)
        if db_notification is None:
            raise HTTPException(status_code=404, detail="Notification not found")
        notification_data = notification_update.model_dump(exclude_unset=True)
        db_notification.sqlmodel_update(notification_data)
        session.add(db_notification)
        session.commit()
        session.refresh(db_notification)
        return db_notification
    except Exception as e:
        print(e)


def delete_notifications(notification_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        db_notification = session.get(Notification, notification_id)
        if db_notification is None:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        session.delete(db_notification)
        session.commit()
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        print(e)
