# Crud Order
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.db.db_connectivity import get_session
from app.models.orders_models import Order, OrderAdd, OrderUpdate
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.producers import get_kafka_producer
from app import order_pb2
from google.protobuf.json_format import MessageToDict


# crud order

async def create_order(order_data:OrderAdd, session:Annotated[Session, Depends(get_session)],
                       producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    
    def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

    order_at_str = datetime_to_iso(order_data.order_date)
    
    order_proto=order_pb2.Order_Proto(user_id=order_data.user_id, order_date=order_at_str, status=order_data.status, total_amount=order_data.total_amount)
    print(f"order_proto: {order_proto}")
    serialized_order=order_proto.SerializeToString()
    print(f"serilized data: {serialized_order}")
    
    try:
        await producer.send_and_wait("order", serialized_order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")
    
    # Convert Protobuf object to a dictionary
    user_dict = MessageToDict(order_proto)

    return user_dict

    # db_order = Order(
    #     user_id=order.user_id,
    #     order_date=order.order_date,
    #     status=order.status,
    #     total_amount=order.total_amount,
    # )
    # session.add(db_order)
    # session.commit()
    # session.refresh(db_order)
    # return db_order
    



def get_orders(session:Annotated[Session, Depends(get_session)]):
    try:
        orders = session.exec(select(Order)).all()
        if not orders:
            raise HTTPException(status_code=404, detail="orders are not exist")
        
        return orders
    except Exception as error:
        print(error)



def get_order_id(order_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        order = session.get(Order, order_id)
        if order is None:
            raise HTTPException(404, "Order not found")
        return order
    except Exception as error:
        print(error)




def update_order(order_id: int, order_update: OrderUpdate, session:Annotated[Session, Depends(get_session)]):
    try:
        db_order = session.get(Order, order_id)
        if db_order is None:
            raise HTTPException(404, "Order not found")
        
        order_data = order_update.model_dump(exclude_unset=True)
        db_order.sqlmodel_update(order_data)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order
    except Exception as error:
        print(error)
        raise HTTPException(400, "Order not found")


def delete_order_id(order_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        order = session.get(Order, order_id)
        if order is None:
            raise HTTPException(404, "Order not found")
        session.delete(order)
        session.commit()
        return {"message": "Order Deleted Successfully"}
    except Exception as error:
        print(error)
        raise HTTPException(400, "Order not found")