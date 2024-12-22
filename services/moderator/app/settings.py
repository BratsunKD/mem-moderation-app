import os

REDIS_URL="redis://redis:6379"
GRAPHITE_HOST = os.getenv('GRAPHITE_HOST', None)
GRAPHITE_PORT = os.getenv('GRAPHITE_PORT', None)