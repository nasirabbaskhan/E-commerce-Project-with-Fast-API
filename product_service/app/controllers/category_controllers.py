import json
from typing import Annotated
from fastapi import Depends, HTTPException
from app import product_pb2
from sqlmodel import Session, select
from app.controllers.auth_admin_controllers import admin_required
from app.db.db_connectivity import get_session
from app.kafka.producers import get_kafka_producer
from app.models.productModel import Category, CategoryAdd, CategoryUpdate
from aiokafka import AIOKafkaProducer # type: ignore
from google.protobuf.json_format import MessageToDict



# Category Crud Opreation Api

async def create_catagory(category_data:CategoryAdd, # type: ignore
                        #   admin_verification: Annotated[dict, Depends(admin_required)],
                         producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
                          session:Annotated[Session, Depends(get_session)]):
    if not category_data:
        raise HTTPException(status_code=404, detail="catagory data missing")
    
     # Check if the user is an admin
    # if not admin_verification:
    #     raise HTTPException(
    #         status_code=403, detail="You are not authorized to create a product!"
    #     )
    
    # varify category is exist already
    db_catagory=session.exec(select(Category).where(Category.name==category_data.name)).all()
    if db_catagory:
        raise HTTPException(status_code=404, detail="Catagory name is already exist")
    
    # category_dict = {field: getattr(category_data, field) for field in category_data.dict()}
    # category_json = json.dumps(category_dict).encode("utf-8")
    # print("categoryJSON:", category_json)
    # # Produce message
    # await producer.send_and_wait("category_service", category_json)
    # # session.add(todo)
    # # session.commit()
    # # session.refresh(todo)
    # return category_data
    
    category_proto=product_pb2.Category_Proto(name=category_data.name, description=category_data.description)
    print(f"product Protobuf: {category_proto}")
    serialized_category_=category_proto.SerializeToString()
    print(f"serilized data: {serialized_category_}")
    
    try:
        await producer.send_and_wait("category", serialized_category_)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")
    
    # Convert Protobuf object to a dictionary
    user_dict = MessageToDict(category_proto)

    return user_dict
    
    # new_catagory=Category(name=category_data.name,description=category_data.description)
    # session.add(new_catagory)
    # session.commit()
    # session.refresh(new_catagory)
    # return new_catagory


def get_category(session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.exec(select(Category)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def get_category_id(category_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Category, category_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Category not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
def update_category_by_id(
    category_id: int, category_update: CategoryUpdate, session:Annotated[Session, Depends(get_session)]):
    # Step 1: Get the Product by ID
    db_category = session.get(Category, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    # Step 2: Update the Product
    hero_data = category_update.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(hero_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def delete_category_by_id(category_id: int, session:Annotated[Session, Depends(get_session)]):
    # Step 1: Get the Product by ID
    product = session.get(Category, category_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Delete the Product
    session.delete(product)
    session.commit()
    return {"message": "Category Deleted Successfully"}