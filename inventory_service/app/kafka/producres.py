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