import json
import asyncio
from aiokafka import AIOKafkaConsumer


class KafkaTextProcessor:
    def __init__(self, consume_topic: str, bootstrap_servers: str, group_id: str, redis):
        self.consume_topic = consume_topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        self.redis = redis

    async def start(self):
        loop = asyncio.get_running_loop()

        self.consumer = AIOKafkaConsumer(
            self.consume_topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=True,
            loop=loop,
        )

        await self.consumer.start()
        print(f"Consumer started for topic: {self.consume_topic}")

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def write_to_redis(self):
        print("start write to redis")
        print(self.redis)
        try:
            async for message in self.consumer:
                try:
                    input_data = json.loads(message.value.decode("utf-8"))
                    user_id = input_data.get("user_id")
                    mem_id = input_data.get("mem_id")
                    text = input_data.get("text")
                    prediction = input_data.get("prediction")

                    # Генерация ключа для Redis
                    redis_key = f"{user_id}:{mem_id}:{text}"

                    # Сохранение в Redis
                    await self.redis.set(redis_key, prediction)
                    print(f"Saved to Redis - Key: {redis_key}, Value: {prediction}")
                except Exception as e:
                    print(f"Error processing message: {e}")
        except Exception as e:
            print(f"Error in consumer loop: {e}")