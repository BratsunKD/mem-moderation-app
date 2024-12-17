import aioredis
import asyncio
from typing import Optional, Union
import json


class RedisClient:
    def __init__(self, redis_url: str, pool: Optional[aioredis.ConnectionPool] = None):
        self.redis_url = redis_url
        self.pool = pool
        self.redis = None

    async def start_connection(self):
        try:
            if self.pool:
                self.redis = aioredis.Redis(connection_pool=self.pool)
            elif self.redis_url:
                self.redis = await aioredis.from_url(self.redis_url)
            else:
                raise ValueError("No redis_url or pool provided")

            print("Redis connection established")
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")

    async def close_connection(self):
        try:
            if self.redis:
                await self.redis.close()
                print("Redis connection closed")
        except Exception as e:
            print(f"Failed to close Redis connection: {e}")

    async def set(self, key: str, value: str):
        serialize_data = json.dumps(value)
        await self.redis.set(key, serialize_data)

    async def get(self, key: str) -> Optional[Union[dict, str]]:
        value = await self.redis.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    async def delete(self, key: str):
        await self.redis.delete(key)
