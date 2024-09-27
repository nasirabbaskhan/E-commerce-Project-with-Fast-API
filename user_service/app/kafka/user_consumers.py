from fastapi import  HTTPException
from aiokafka import AIOKafkaConsumer # type: ignore
from app import user_pb2
from app.db.db_connectivity import get_session
from app.models.user_models import User


async def user_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="user1_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_user = user_pb2.User_Proto()
            new_user.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_user}")
            with next(get_session()) as session:
                user_todo= User(user_name=new_user.user_name,user_email=new_user.user_email, user_password=new_user.user_password, phone_number=new_user.phone_number )
                if user_todo:
                    session.add(user_todo)
                    session.commit()
                    session.refresh(user_todo)
                    return user_todo
                else:
                    raise HTTPException(status_code=404, detail="Todo not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()