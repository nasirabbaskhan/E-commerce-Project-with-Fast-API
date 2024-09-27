from fastapi import  HTTPException
from aiokafka import AIOKafkaConsumer # type: ignore
from app import product_pb2
from app.db.db_connectivity import get_session
from app.models.productModel import Category, Product, Rating, Review



async def category_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="category_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_category = product_pb2.Category_Proto()
            new_category.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_category}")
            with next(get_session()) as session:
                category= Category(name=new_category.name,description=new_category.description )
                if category:
                    session.add(category)
                    session.commit()
                    session.refresh(category)
                    return category
                else:
                    raise HTTPException(status_code=404, detail="Todo not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
        
        
async def product_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_product = product_pb2.Product_Proto()
            new_product.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_product}")
            with next(get_session()) as session:
                product= Product(name=new_product.name, description=new_product.description,
                                        price=new_product.price, available=new_product.available,category_id=new_product.category_id,
                                        brand=new_product.brand, weight=new_product.weight, sku=new_product.sku)
                print("added prodect", product) 
                if product:
                    session.add(product)
                    session.commit()
                    session.refresh(product)
                    return product
                else:
                    raise HTTPException(status_code=404, detail="product not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
        
        
async def rating_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="rating_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_rating = product_pb2.Rating_Proto()
            new_rating.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_rating}")
            with next(get_session()) as session:
                rating= Rating(rating=new_rating.rating, product_id=new_rating.product_id)
                print("added rating", rating) 
                if rating:
                    session.add(rating)
                    session.commit()
                    session.refresh(rating)
                    return rating
                else:
                    raise HTTPException(status_code=404, detail="rating not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
        
        
async def review_consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="review_group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            new_review = product_pb2.Review_Proto()
            new_review.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_review}")
            with next(get_session()) as session:
                review= Review(review_text=new_review.review_text, product_id=new_review.product_id)
                print("added review", review) 
                if review:
                    session.add(review)
                    session.commit()
                    session.refresh(review)
                    return review
                else:
                    raise HTTPException(status_code=404, detail="review not created")
                    
    
        # Here you can add code to process each message.
        # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()