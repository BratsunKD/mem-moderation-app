import json
import asyncio
import os
import time
from statsd import StatsClient
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


MODEL_TYPE = 'bert'


async def monitor_kafka_lag(consumer: AIOKafkaConsumer, statsd):
    print("monitor_kafka_lag started")
    try:
        while True:
            try:
                metrics = await consumer.metrics()
                print("METRICS fetched:", metrics)
                if 'consumer-lag' in metrics:
                    for topic, partitions in metrics['consumer-lag'].items():
                        for partition, lag in partitions.items():
                            statsd.gauge(f'kafka.topic.{topic}.lag', lag)
                            print(f"Sent gauge metric: kafka.topic.{topic}.lag = {lag}")
                else:
                    print("No 'consumer-lag' in metrics")
            except Exception as e:
                print(f"Error while fetching metrics: {e}")

            await asyncio.sleep(3)
    except Exception as e:
        print(f"Error in monitor_kafka_lag: {e}")


class KafkaTextProcessor:
    def __init__(self, consume_topic: str, produce_topic: str, bootstrap_servers: str, group_id: str, model, statsd):
        self.consume_topic = consume_topic
        self.produce_topic = produce_topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        self.producer = None
        self.model = model
        self.statsd = statsd

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
                self.statsd.incr('worker.predict.count')
                try:
                    input_data = json.loads(message.value.decode("utf-8"))
                    text = input_data.get("text", "")
                    print(f"Received message: {input_data}")

                    tic = time.perf_counter()
                    prediction = self.model.predict(text)
                    toc = time.perf_counter()
                    self.statsd.timing('worker.predict.timing.inference', toc - tic)

                    print(f"Prediction OK")

                    result = {
                        "text": text,
                        "prediction": [p.item() for p in prediction],
                        "user_id": input_data.get("user_id", ""),
                        "text_id": input_data.get("text_id", ""),
                        "metadata": {"source_offset": message.offset},
                    }
                    print(f"Processed result: {result}")

                    await self.send_to_producer(result)
                    self.statsd.incr('worker.predict.produce.success.count')
                except Exception as e:
                    self.statsd.incr('worker.predict.produce.error.count')
                    print(f"Error processing message: {e}")
        except Exception as e:
            print(f"Error in consumer loop: {e}")
