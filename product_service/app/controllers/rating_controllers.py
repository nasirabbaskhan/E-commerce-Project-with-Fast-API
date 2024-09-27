from typing import Annotated

from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.db.db_connectivity import get_session
from app.models.productModel import  Product, Rating, RatingAdd, RatingUpdate
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.producers import get_kafka_producer
from app import product_pb2
from google.protobuf.json_format import MessageToDict




# # Rating Crud Opreation

async def add_rating(rating_data:RatingAdd,session:Annotated[Session, Depends(get_session)],
                     producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    try:
        validate_product_id = session.get(Product, rating_data.product_id)
        if validate_product_id is None:
            raise HTTPException(status_code=404, detail="Product not found so you can not add the rating!")
        
        
        rating_proto=product_pb2.Rating_Proto(rating=rating_data.rating, product_id=rating_data.product_id)
        print(f"rating_proto: {rating_proto}")
        serialized_rating_=rating_proto.SerializeToString()
        print(f"serilized data: {serialized_rating_}")
        
        try:
            await producer.send_and_wait("rating", serialized_rating_)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")
        
        # Convert Protobuf object to a dictionary
        user_dict = MessageToDict(rating_proto)

        return user_dict
        
        
        
        # db_user = Rating(
        #     rating=rating.rating,
        #     product_id=rating.product_id,
            
        # )
        # session.add(db_user)
        # session.commit()
        # session.refresh(db_user)
        # return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
def get_rating(session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.exec(select(Rating)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_rating_id(rating_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Rating, rating_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Rating not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





def update_rating_by_id(rating_id: int, rating_update: RatingUpdate, session:Annotated[Session, Depends(get_session)]):
    # Step 1: Get the Product by ID
    rating = session.get(Rating, rating_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    # Step 2: Update the Product
    hero_data = rating_update.model_dump(exclude_unset=True)
    rating.sqlmodel_update(hero_data)
    session.add(rating)
    session.commit()
    session.refresh(rating)
    return rating


def delete_rating_by_id(rating_id: int,  session:Annotated[Session, Depends(get_session)]):
    # Step 1: Get the Product by ID
    rating = session.get(Rating, rating_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    # Step 2: Delete the Product
    session.delete(rating)
    session.commit()
    return {"message": "Rating Deleted Successfully"}