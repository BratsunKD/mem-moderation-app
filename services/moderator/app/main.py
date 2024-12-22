from fastapi import FastAPI
import json

import asyncio
import aioredis
from app.schemas import Prediction, Message
from app.redis_client import RedisClient
from app.settings import REDIS_URL
from contextlib import asynccontextmanager


pool = aioredis.ConnectionPool.from_url(REDIS_URL, max_connections=10)
redis = RedisClient(REDIS_URL, pool=pool)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis.start_connection()
    yield
    await redis.close_connection()


app = FastAPI(lifespan=lifespan)


@app.post("/get-prediction/")
async def get_prediction(message: Message):
    user_id = message.user_id
    mem_id = message.mem_id
    text = message.text

    redis_key = f"{user_id}:{mem_id}:{text}"
    result = await redis.get(redis_key)
    if result is None:
        return result
    return float(result)



