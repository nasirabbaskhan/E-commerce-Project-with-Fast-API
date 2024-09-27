# Crud Shipment
from datetime import datetime
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.db.db_connectivity import get_session
from app.models.orders_models import Order, Shipment, ShipmentAdd, ShipmentUpdate
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.producers import get_kafka_producer
from app import order_pb2
from google.protobuf.json_format import MessageToDict



#crud shipment

async def create_shipment(shipment:ShipmentAdd , session: Annotated[Session, Depends(get_session)],
                          producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    try:
        validate_order_id = session.get(Order, shipment.order_id)
        if validate_order_id is None:
            raise HTTPException(404, "Order not found")
        
        
        def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

        shipment_date_at_str = datetime_to_iso(shipment.shipment_date)
        delivery_date_at_str = datetime_to_iso(shipment.delivery_date)
        
        shipment_proto=order_pb2.Shipment_Proto(order_id=shipment.order_id, shipment_date=shipment_date_at_str, delivery_date=delivery_date_at_str ,status=shipment.status)
        print(f"order_proto: {shipment_proto}")
        serialized_shipment=shipment_proto.SerializeToString()
        print(f"serialized_shipment: {serialized_shipment}")

        try:
            await producer.send_and_wait("shipment", serialized_shipment)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")

        # Convert Protobuf object to a dictionary
        user_dict = MessageToDict(shipment_proto)

        return user_dict
        
        
        # db_shipment = Shipment(
        #     order_id=shipment.order_id,
        #     shipment_date=shipment.shipment_date,
        #     delivery_date=shipment.delivery_date,
        #     status=shipment.status,
        # )
        # session.add(db_shipment)
        # session.commit()
        # session.refresh(db_shipment)
        # return db_shipment
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")

def get_shipments(session: Annotated[Session, Depends(get_session)]):
    try:
        shipments = session.exec(select(Shipment)).all()
        if shipments is None:
            raise HTTPException(status_code=404, detail="No shipments found")
        return shipments
    except Exception as error:
        print(error)


def get_shipment_id(shipment_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        shipment = session.get(Shipment, shipment_id)
        if shipment is None:
            raise HTTPException(404, "Shipment not found")
        return shipment
    except Exception as error:
        print(error)




def update_shipment(
    shipment_id: int, shipment_update: ShipmentUpdate, session: Annotated[Session, Depends(get_session)]
):
    try:
        db_shipment = session.get(Shipment, shipment_id)
        if db_shipment is None:
            raise HTTPException(404, "Shipment not found")
        shipment_data = shipment_update.model_dump(exclude_unset=True)
        db_shipment.sqlmodel_update(shipment_data)
        session.add(db_shipment)
        session.commit()
        session.refresh(db_shipment)
        return db_shipment
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def delete_shipment_id(shipment_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        shipment = session.get(Shipment, shipment_id)
        if shipment is None:
            raise HTTPException(404, "Shipment not found")
        session.delete(shipment)
        session.commit()
        return {"message": "Shipment Deleted Successfully"}
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def validate_by_id(order_id: int, session: Session):
    try:
        order = session.get(Order, id)
        if order is None:
            raise HTTPException(404, "Order not found")
        return order
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")
