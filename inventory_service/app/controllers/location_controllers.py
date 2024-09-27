from typing import Annotated
from fastapi import Depends, HTTPException
from app.db.db_connectivity import get_session
from app.models.inventory_model import Location, LocationAdd, LocationUpdate
from sqlmodel import Session, select
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.producres import get_kafka_producer
from app import inventory_pb2
from google.protobuf.json_format import MessageToDict



# Crud Location

async def add_location(location_data:LocationAdd, session:Annotated[Session, Depends(get_session)],
                       producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    try:
        # varify location is already exist
        db_location = session.exec(select(Location).where(Location.location_name==location_data.location_name)).one_or_none()
        if db_location:
            raise HTTPException(status_code=404, detail="This Location is already exist")
        
        location_proto=inventory_pb2.Location_Proto(location_name=location_data.location_name, address=location_data.address)
        print(f"notification_proto: {location_proto}")
        serialized_location=location_proto.SerializeToString()
        print(f"serialized_notification: {serialized_location}")

        try:
            await producer.send_and_wait("location", serialized_location)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")

        # Convert Protobuf object to a dictionary
        user_dict = MessageToDict(location_proto)

        return user_dict
        
        # db_user = Location(
        #     location_name=location.location_name,
        #     address=location.address,
            
        # )
        # session.add(db_user)
        # session.commit()
        # session.refresh(db_user)
        # return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def get_location(session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.exec(select(Location)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_location_id(location_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Location, location_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Location not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





def update_location_by_id(
    location_id: int, location_update: LocationUpdate, session:Annotated[Session, Depends(get_session)]):
    try:
        # Step 1: Get the Product by ID
        product = session.get(Location, location_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Location not found")
        # Step 2: Update the Product
        location_data = location_update.model_dump(exclude_unset=True)
        product.sqlmodel_update(location_data)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    # return {"message": "Product updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_location_by_id(location_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        location = session.get(Location, location_id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        session.delete(location)
        session.commit()
        return {"message": "Location deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
