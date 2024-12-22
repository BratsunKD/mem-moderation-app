import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

PRODUCE_TOPIC = os.getenv("TEXT_TOPIC")

GRAPHITE_HOST = os.getenv('GRAPHITE_HOST', None)
GRAPHITE_PORT = os.getenv('GRAPHITE_PORT', None)
MODERATOR_URL = "http://moderator:4000/get-prediction/"
