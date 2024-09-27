

from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.db.db_connectivity import get_session
from app.models.orders_models import Order, OrderItem, OrderItemAdd, OrderItemUpdate
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.producers import get_kafka_producer
from app import order_pb2
from google.protobuf.json_format import MessageToDict

# Crud OrderItems
async def create_order_item(order_item:OrderItemAdd, session:Annotated[Session, Depends(get_session)],
                            producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    try:
        validate_order_id = session.get(Order, order_item.order_id)
        if validate_order_id is None:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order_item_proto=order_pb2.OrderItem_Proto(order_id=order_item.order_id, product_id=order_item.product_id, quantity=order_item.quantity, price=order_item.price, total_price=order_item.quantity*order_item.price)
        print(f"order_item_proto: {order_item_proto}")
        serialized_orser_item=order_item_proto.SerializeToString()
        print(f"serilized data: {serialized_orser_item}")
        
        try:
            await producer.send_and_wait("orderItem", serialized_orser_item)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")
        
        # Convert Protobuf object to a dictionary
        user_dict = MessageToDict(order_item_proto)

        return user_dict
        
    #     db_order_item = OrderItem(
    #         order_id=order_item.order_id,
    #         product_id=order_item.product_id,
    #         quantity=order_item.quantity,
    #         price=order_item.price,
    #         total_price=order_item.quantity*order_item.price,
    #     )
    #     session.add(db_order_item)
    #     session.commit()
    #     session.refresh(db_order_item)
    #     return db_order_item
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")
    

def get_order_items(session:Annotated[Session, Depends(get_session)]):
    try:
        order_items = session.exec(select(OrderItem)).all()
        if order_items is None:
            raise HTTPException(404, "No order items found")
        return order_items
    except Exception as error:
        print(error)


def get_order_item_id(order_item_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        order_item = session.get(OrderItem, order_item_id)
        if order_item is None:
            raise HTTPException(404, "Order item not found")
        return order_item
    except Exception as error:
        print(error)



def update_order_item(order_item_id: int, order_item_update: OrderItemUpdate, session:Annotated[Session, Depends(get_session)]):
    try:
        db_order_item = session.get(OrderItem, order_item_id)
        if db_order_item is None:
            raise HTTPException(404, "Order item not found")
        
        order_item_data = order_item_update.model_dump(exclude_unset=True)
        db_order_item.sqlmodel_update(order_item_data)
        session.add(db_order_item)
        session.commit()
        session.refresh(db_order_item)
        return db_order_item
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def delete_order_item_id(order_item_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        order_item = session.get(OrderItem, order_item_id)
        if order_item is None:
            raise HTTPException(404, "Order item not found")
        session.delete(order_item)
        session.commit()
        return {"message": "Order item Deleted Successfully"}
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")