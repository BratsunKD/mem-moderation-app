import asyncio

from app import settings
from app.kafka_processor import KafkaTextProcessor
from fastapi import FastAPI



KAFKA_CONSUMER_GROUP = "text_prediction_consumer"

# app = FastAPI()


async def main():
    consumer = KafkaTextProcessor(
        consume_topic=settings.CONSUME_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_CONSUMER_GROUP,
        redis_url=settings.REDIS_URL,
    )

    await consumer.start()
    try:
        await consumer.process_messages()
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
    print(1)