import json
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from app import settings

KAFKA_CONSUMER_GROUP = "text_processing_consumer"



class MockModel:
    def __init__(self, weights_path: str):
        print(f"Initializing model with weights from {weights_path}")
        self.weights_path = weights_path

    def predict(self, text: str) -> int:
        return len(text)



MODEL_WEIGHTS_PATH = "./weights/model_weights"
model = MockModel(weights_path=MODEL_WEIGHTS_PATH)


class KafkaTextProcessor:
    def __init__(self, consume_topic: str, produce_topic: str, bootstrap_servers: str, group_id: str):
        self.consume_topic = consume_topic
        self.produce_topic = produce_topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        self.producer = None

    async def start(self):
        loop = asyncio.get_running_loop()

        self.consumer = AIOKafkaConsumer(
            self.consume_topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=True,
            loop=loop,
        )
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            loop=loop,
        )

        await self.consumer.start()
        await self.producer.start()
        print(f"Consumer started for topic: {self.consume_topic}")
        print(f"Producer initialized for topic: {self.produce_topic}")

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
        if self.producer:
            await self.producer.stop()
        print("Consumer and producer stopped.")

    async def send_to_producer(self, result: dict):
        try:
            message = json.dumps(result).encode("utf-8")
            await self.producer.send_and_wait(
                topic=self.produce_topic,
                value=message,
            )
            print(f"Message sent to topic {self.produce_topic}: {result}")
        except Exception as e:
            print(f"Error sending message to producer: {e}")

    async def process_messages(self):
        try:
            async for message in self.consumer:
                try:
                    input_data = json.loads(message.value.decode("utf-8"))
                    text = input_data.get("text", "")
                    print(f"Received message: {input_data}")

                    prediction = model.predict(text)
                    result = {
                        "original_text": text,
                        "prediction": prediction,
                        "metadata": {"source_offset": message.offset},
                    }
                    print(f"Processed result: {result}")

                    await self.send_to_producer(result)
                except Exception as e:
                    print(f"Error processing message: {e}")
        except Exception as e:
            print(f"Error in consumer loop: {e}")


async def main():
    processor = KafkaTextProcessor(
        consume_topic=settings.CONSUME_TOPIC,
        produce_topic=settings.PRODUCE_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
    )

    await processor.start()
    try:
        await processor.process_messages()
    finally:
        await processor.stop()


if __name__ == "__main__":
    asyncio.run(main())

