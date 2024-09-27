from fastapi import  HTTPException
from aiokafka import AIOKafkaConsumer # type: ignore
from app import notification_pb2
from app.db.db_connectivity import get_session

from app.models.notification_models import Notification
# from app.models.productModel import Category, Product, Rating, Review



async def notification_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="notification_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_notification =notification_pb2.Notification_Proto()
            new_notification.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_notification}")
            with next(get_session()) as session:
                notification= Notification(user_id=new_notification.user_id, order_id=new_notification.order_id, message=new_notification.message, read=new_notification.read)
                if notification:
                    session.add(notification)
                    session.commit()
                    session.refresh(notification)
                    return notification
                else:
                    raise HTTPException(status_code=404, detail="Todo not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()