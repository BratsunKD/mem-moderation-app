from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import FastAPI, Depends
from app.schemas import Message
from app.producer import get_producer
import json

if TYPE_CHECKING:
    from app.producer import AIOWebProducer


app = FastAPI()


@app.post("/text-moderation")
async def send(message: Message, producer: AIOWebProducer = Depends(get_producer)) -> None:
    message_to_produce = json.dumps(message.model_dump()).encode(encoding="utf-8")
    print("OK", message_to_produce)
    await producer.send(value=message_to_produce)


@app.post("/text-moderation")
async def send(message: Message) -> None:
    message_to_produce = json.dumps(message.model_dump()).encode(encoding="utf-8")



