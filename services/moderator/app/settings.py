import os

KAFKA_BOOTSTRAP_SERVERS=os.getenv("KAFKA_BOOTSTRAP_SERVERS")
CONSUME_TOPIC=os.getenv("PREDICTION_TOPIC")
KAFKA_CONSUMER_GROUP="text_prediction_consumer"
REDIS_URL="redis://localhost:6379"