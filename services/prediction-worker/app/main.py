from app.settings import REDIS_URL, CONSUME_TOPIC, KAFKA_BOOTSTRAP_SERVERS

import aioredis
import asyncio
from app.kafka_processor import KafkaTextProcessor
from app.redis_client import RedisClient
from app.settings import GRAPHITE_HOST, GRAPHITE_PORT
from statsd import StatsClient

KAFKA_CONSUMER_GROUP = "text_prediction_consumer"


kafka_redis_pool = aioredis.ConnectionPool.from_url(REDIS_URL, max_connections=10)

kafka_redis_client = RedisClient(REDIS_URL, pool=kafka_redis_pool)
statsd = StatsClient(GRAPHITE_HOST, int(GRAPHITE_PORT), prefix='toxic-detector')


async def main():
    await kafka_redis_client.start_connection()

    processor = KafkaTextProcessor(
        consume_topic=CONSUME_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        redis=kafka_redis_client,
        statsd=statsd,
    )

    await processor.start()
    try:
        await processor.write_to_redis()
    finally:
        await processor.stop()

    await kafka_redis_client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())

