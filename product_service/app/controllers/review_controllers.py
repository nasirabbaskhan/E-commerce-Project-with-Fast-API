from typing import Annotated

from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.db.db_connectivity import get_session
from app.models.productModel import  Product,  Review, ReviewAdd, ReviewUpdate
from aiokafka import AIOKafkaProducer # type: ignore
from app.kafka.producers import get_kafka_producer
from app import product_pb2
from google.protobuf.json_format import MessageToDict



# # Review Crud Opreation

async def add_review(review_data:ReviewAdd, session:Annotated[Session, Depends(get_session)],
                     producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    try:
        validate_product_id = session.get(Product, review_data.product_id)
        if validate_product_id is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        review_proto=product_pb2.Review_Proto(review_text=review_data.review_text, product_id=review_data.product_id)
        print(f"rating_proto: {review_proto}")
        serialized_review=review_proto.SerializeToString()
        print(f"serilized data: {serialized_review}")
        
        try:
            await producer.send_and_wait("reviews", serialized_review)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send Kafka message: {str(e)}")
        
        # Convert Protobuf object to a dictionary
        user_dict = MessageToDict(review_proto)

        return user_dict
        
        
    #     db_user = Review(
    #         review_text=review.review_text,
    #         product_id=review.product_id,
            
    #     )
    #     session.add(db_user)
    #     session.commit()
    #     session.refresh(db_user)
    #     return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_review(session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.exec(select(Review)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_review_id(review_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Review, review_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Review not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




def update_review_by_id(review_id: int, review_update: ReviewUpdate, session:Annotated[Session, Depends(get_session)]):
    # Step 1: Get the Product by ID
    review = session.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    # Step 2: Update the Product
    hero_data = review_update.model_dump(exclude_unset=True)
    review.sqlmodel_update(hero_data)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


def delete_review_by_id(review_id: int, session:Annotated[Session, Depends(get_session)]):
    # Step 1: Get the Product by ID
    review = session.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    # Step 2: Delete the Product
    session.delete(review)
    session.commit()
    return {"message": "Review Deleted Successfully"}
