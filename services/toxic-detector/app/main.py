import asyncio

import os
from statsd import StatsClient

from app import settings
from app.model import BertModerator
from app.kafka_processor import KafkaTextProcessor
from app.settings import GRAPHITE_HOST, GRAPHITE_PORT, MODEL_NAME
from transformers import pipeline


KAFKA_CONSUMER_GROUP = "text_processing_consumer"
MODEL_WEIGHTS_PATH = "model_weights/bert_toxic_model.pt"

statsd = StatsClient(GRAPHITE_HOST, int(GRAPHITE_PORT), prefix='toxic-detector')


async def main():
    model = BertModerator(weights_path=MODEL_WEIGHTS_PATH, name=MODEL_NAME)

    processor = KafkaTextProcessor(
        consume_topic=settings.CONSUME_TOPIC,
        produce_topic=settings.PRODUCE_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        model=model,
        statsd=statsd,
    )

    await processor.start()
    try:
        await processor.process_messages()
    finally:
        await processor.stop()


if __name__ == "__main__":
    asyncio.run(main())

