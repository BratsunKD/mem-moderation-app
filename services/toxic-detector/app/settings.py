import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

CONSUME_TOPIC = os.getenv("TEXT_TOPIC")
PRODUCE_TOPIC = os.getenv("PREDICTION_TOPIC")

GRAPHITE_HOST = os.getenv('GRAPHITE_HOST', None)
GRAPHITE_PORT = os.getenv('GRAPHITE_PORT', None)

MODEL_NAME = 'bert-base-uncased'
