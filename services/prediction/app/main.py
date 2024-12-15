import asyncio

from app import settings
from app.model import MockModel
from app.kafka_processor import KafkaTextProcessor


KAFKA_CONSUMER_GROUP = "text_processing_consumer"
MODEL_WEIGHTS_PATH = "./weights/model_weights"



async def main():
    model = MockModel(weights_path=MODEL_WEIGHTS_PATH)

    processor = KafkaTextProcessor(
        consume_topic=settings.CONSUME_TOPIC,
        produce_topic=settings.PRODUCE_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        model=model,
    )

    await processor.start()
    try:
        await processor.process_messages()
    finally:
        await processor.stop()


if __name__ == "__main__":
    asyncio.run(main())

