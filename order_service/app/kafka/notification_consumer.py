from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import logging
from app import notification_pb2
from app.db.db_connectivity import get_session
from app.controllers.users_controllers import validate_by_id

logging.basicConfig(level=logging.INFO)


async def notification_consume_messages(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="notification1_group",
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            logger.info("consumed: %s", msg.value)
            notification_add = notification_pb2.Notification_Proto()
            notification_add.ParseFromString(msg.value)
            logger.debug("Deserialized Data: %s", notification_add)

            user_id = notification_add.user_id
            logger.info("USER ID: %s", user_id)

            with next(get_session()) as session:
                try:
                    validate_data = validate_by_id(user_id=user_id, session=session)
                    if validate_data is None:
                        logger.info("User not found")
                    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
                    await producer.start()
                    try:
                        await producer.send_and_wait("notification", msg.value)
                    finally:
                        await producer.stop()
                except Exception as e:
                    logger.error("Error: %s", str(e))

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
