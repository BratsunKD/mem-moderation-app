from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import FastAPI, Depends
from app.schemas import Message
from app.producer import get_producer
import os
import httpx
import time
from statsd import StatsClient

from app.settings import GRAPHITE_HOST, GRAPHITE_PORT, MODERATOR_URL
import json

if TYPE_CHECKING:
    from app.producer import AIOWebProducer


app = FastAPI()
statsd = StatsClient(GRAPHITE_HOST, int(GRAPHITE_PORT), prefix='toxic-detector')


@app.post("/text-moderation/")
async def send(message: Message, producer: AIOWebProducer = Depends(get_producer)) -> None:
    statsd.incr('api.request.count')
    tic = time.perf_counter()
    try:
        message_to_produce = json.dumps(message.model_dump()).encode(encoding="utf-8")
        await producer.send(value=message_to_produce)
        toc = time.perf_counter()
        statsd.timing('api.request.timing.produce_text', toc - tic)
    except Exception as e:
        statsd.incr('api.request.error.produce_text')
        print(f"Error producing message: {e}")


@app.post("/get-result/")
async def get(message: Message):
    statsd.incr('api.request.result.count')
    tic = time.perf_counter()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(MODERATOR_URL, json=message.dict())
        toc = time.perf_counter()
        statsd.timing('api.request.result.timing.get_result', toc - tic)
        prediction = response.json()
        return {"prediction": prediction}
    except Exception as e:
        statsd.incr('api.request.error.get_result')
        print(f"Error get_result message: {e}")
