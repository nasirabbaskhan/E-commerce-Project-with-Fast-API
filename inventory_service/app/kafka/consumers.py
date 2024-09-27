from fastapi import  HTTPException
from aiokafka import AIOKafkaConsumer # type: ignore
from app import inventory_pb2
from app.db.db_connectivity import get_session
from app.models.inventory_model import Location , Inventory

# from app.models.notification_models import Notification
# from app.models.productModel import Category, Product, Rating, Review



async def inventory_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="inventory_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_inventory =inventory_pb2.Inventory_Proto()
            new_inventory.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_inventory}")
            with next(get_session()) as session:
                inventory= Inventory(product_id=new_inventory.product_id, quantity=new_inventory.quantity, location_id=new_inventory.location_id)
                if inventory:
                    session.add(inventory)
                    session.commit()
                    session.refresh(inventory)
                    return inventory
                else:
                    raise HTTPException(status_code=404, detail="Todo not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
        
        
        
async def location_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="location_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_location =inventory_pb2.Location_Proto()
            new_location.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_location}")
            with next(get_session()) as session:
                location= Location(location_name=new_location.location_name, address=new_location.address)
                if location:
                    session.add(location)
                    session.commit()
                    session.refresh(location)
                    return location
                else:
                    raise HTTPException(status_code=404, detail="Todo not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()