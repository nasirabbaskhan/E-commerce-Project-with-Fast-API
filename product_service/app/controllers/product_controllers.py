
from typing import Annotated
from app import product_pb2
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.db.db_connectivity import get_session
from app.models.productModel import Category, CategoryAdd, CategoryUpdate, Product, ProductAdd, ProductUpdate, Rating, RatingAdd, RatingUpdate, Review, ReviewAdd, ReviewUpdate
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.producers import get_kafka_producer
from google.protobuf.json_format import MessageToDict


# Product Crud opreation Api

async def create_product(product_data:ProductAdd, 
                         producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
                         session:Annotated[Session, Depends(get_session)]):
    if not product_data:
        raise HTTPException(status_code=404, detail="product_data missing")
    
    # varify catagory_id is exist or not
    validate_category_id = session.get(Category, product_data.category_id)
    if validate_category_id is None:
        raise HTTPException(status_code=404, detail="catagery of gevin id is not exist")
    
    product_proto=product_pb2.Product_Proto(name=product_data.name, description=product_data.description,
                                            price=product_data.price, available=product_data.available,category_id=product_data.category_id,
                                            brand=product_data.brand, weight=product_data.weight, sku=product_data.sku)
    print(f"product Protobuf: {product_proto}")
    serialized_product=product_proto.SerializeToString()
    print(f"serilized data: {serialized_product}")
    
    try:
        await producer.send_and_wait("product", serialized_product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")
    
    # Convert Protobuf object to a dictionary
    user_dict = MessageToDict(product_proto)

    return user_dict
    
    
  
    # new_product=Product(
    #     name=product_data.name,
    #     description=product_data.description,
    #     price=product_data.price,
    #     weight=product_data.weight,
    #     sku=product_data.sku,
    #     available=product_data.available,
    #     brand=product_data.brand, 
    #     category_id=product_data.category_id, )
    # session.add(new_product)
    # session.commit()
    # session.refresh(new_product)
    # return new_product


def get_product(session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.exec(select(Product)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   
    
    
def get_product_id(product_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Product, product_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Product not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   
  
    
    
 
def update_product_by_id(
    product_id: int, product_update: ProductUpdate, session:Annotated[Session, Depends(get_session)]):
    # Step 1: Get the Product by ID
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Update the Product
    hero_data = product_update.model_dump(exclude_unset=True)
    product.sqlmodel_update(hero_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def delete_product_by_id(product_id: int, session:Annotated[Session, Depends(get_session)]):
    # Step 1: Get the Product by ID
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Delete the Product
    session.delete(product)
    session.commit()
    return {"message": "Product Deleted Successfully"}


def validate_product_id(product_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

   


    


