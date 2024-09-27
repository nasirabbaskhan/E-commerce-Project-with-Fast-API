from typing import Annotated
from fastapi import Depends, HTTPException
from app.db.db_connectivity import get_session
from app.models.inventory_model import Inventory, InventoryAdd, InventoryUpdate, Location
from sqlmodel import Session, select
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.producres import get_kafka_producer
from app import inventory_pb2
from google.protobuf.json_format import MessageToDict





# Crud inventory

async def add_inventory(inventory:InventoryAdd,session:Annotated[Session, Depends(get_session)],
                        producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    try:
        validate_location_id = session.get(Location, inventory.location_id)
        if validate_location_id is None:
            raise HTTPException(status_code=404, detail="Location not found")
        
        inventory_proto=inventory_pb2.Inventory_Proto(product_id=inventory.product_id, quantity=inventory.quantity, location_id=inventory.location_id)
        print(f"notification_proto: {inventory_proto}")
        serialized_inventory=inventory_proto.SerializeToString()
        print(f"serialized_notification: {serialized_inventory}")

        try:
            await producer.send_and_wait("inventory", serialized_inventory)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")

        # Convert Protobuf object to a dictionary
        user_dict = MessageToDict(inventory_proto)

        return user_dict
        
        # db_user = Inventory(
        #     location_id=inventory.location_id,
        #     product_id=inventory.product_id,
        #     quantity=inventory.quantity,
           
        # )
        # session.add(db_user)
        # session.commit()
        # session.refresh(db_user)
        # return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
def get_inventory(session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.exec(select(Inventory)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_inventory_id(inventory_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Inventory, inventory_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Inventory not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





def update_inventory_by_id(
    inventory_id: int, inventory_update: InventoryUpdate, session:Annotated[Session, Depends(get_session)]):
    try:
        # Step 1: Get the Product by ID
        inventory = session.get(Inventory, inventory_id)
        if inventory is None:
            raise HTTPException(status_code=404, detail="Inventory not found")
        # Step 2: Update the Product
        hero_data = inventory_update.model_dump(exclude_unset=True)
        inventory.sqlmodel_update(hero_data)
        session.add(inventory)
        session.commit()
        session.refresh(inventory)
        return inventory

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_inventory_by_id(inventory_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        inventory = session.get(Inventory, inventory_id)
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")
        session.delete(inventory)
        session.commit()
        return {"message": "Inventory deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
