from aiokafka import AIOKafkaConsumer
from app import settings
import asyncio

event_loop = asyncio.get_event_loop()


class AIOWebConsumer(object):
    def __init__(self):
        self.__consumer = AIOKafkaConsumer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            loop=event_loop,
        )
        self.__consume_topic = settings.CONSUME_TOPIC

    async def start(self) -> None:
        await self.__consumer.start()

    async def stop(self) -> None:
        await self.__consumer.stop()

    async def read(self):
        message_value = None
        await self.__consumer.start()
        try:
            async for msg in self.__consumer:
                print(
                    "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
                        msg.topic, msg.partition, msg.offset, msg.key, msg.value,
                        msg.timestamp)
                )
                message_value = msg.value
            return message_value
        finally:
            await self.__consumer.stop()


def get_consumer() -> AIOWebConsumer:
    return AIOWebConsumer()
