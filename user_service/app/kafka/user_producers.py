from typing import Any
from aiokafka import AIOKafkaProducer # type: ignore
from fastapi import Depends




async def get_kafka_producer():
    producer= AIOKafkaProducer(bootstrap_servers="broker:19092")
    await producer.start()
    print("producing starting........")
    try:
        yield producer
        
    finally:
        print("producer is stoped....")
        await producer.stop()
        
        
        
# async def producer(message:Any, topic:str, aio_producr:AIOKafkaProducer= Depends(get_kafka_producer)):
#     try:
#         result= await aio_producr.send_and_wait(topic, message.encode("utf-8"))
#     except:
#         print("error is occur")
#     finally:
#         await aio_producr.stop()
#         return result
    

