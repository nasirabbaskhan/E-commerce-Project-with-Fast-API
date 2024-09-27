from fastapi import  HTTPException
from aiokafka import AIOKafkaConsumer # type: ignore
from app import order_pb2
from app.db.db_connectivity import get_session

from app.models.orders_models import OrderItem, Order , Shipment
# from app.models.productModel import Category, Product, Rating, Review



async def orderItem_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="orderItem_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_orderItem = order_pb2.OrderItem_Proto()
            new_orderItem.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_orderItem}")
            with next(get_session()) as session:
                order_item= OrderItem(order_id=new_orderItem.order_id, product_id=new_orderItem.product_id, quantity=new_orderItem.quantity, price=new_orderItem.price, total_price=new_orderItem.total_price )
                if order_item:
                    session.add(order_item)
                    session.commit()
                    session.refresh(order_item)
                    return order_item
                else:
                    raise HTTPException(status_code=404, detail="Todo not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
        
        
        
async def order_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_order = order_pb2.Order_Proto()
            new_order.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_order}")
            with next(get_session()) as session:
                order= Order(user_id=new_order.user_id, order_date=new_order.order_date, status=new_order.status, total_amount=new_order.total_amount )
                if order:
                    session.add(order)
                    session.commit()
                    session.refresh(order)
                    return order
                else:
                    raise HTTPException(status_code=404, detail="Todo not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
        
        
        
        
async def shipment_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="shipment_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_shipment = order_pb2.Shipment_Proto()
            new_shipment.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_shipment}")
            with next(get_session()) as session:
                shipment= Shipment(order_id=new_shipment.order_id, shipment_date=new_shipment.shipment_date, delivery_date=new_shipment.delivery_date ,status=new_shipment.status )
                if shipment:
                    session.add(shipment)
                    session.commit()
                    session.refresh(shipment)
                    return shipment
                else:
                    raise HTTPException(status_code=404, detail="Todo not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
        