from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING
from fastapi import FastAPI, Depends

from app.schemas import Message, ModelPredict

from app.producer import get_producer
from app.consumer import get_consumer


if TYPE_CHECKING:
    from app.producer import AIOWebProducer
    from app.consumer import AIOWebConsumer


app = FastAPI()



async def get_text(consumer: AIOWebConsumer = get_consumer()) -> None:
    res = await consumer.read()
    print(res)
    print("OK получили результат из топика input_text", res)

    # Запрос к модельки и вызов асинхронной set_text


async def set_text(predict: ModelPredict, producer: AIOWebProducer = Depends(get_producer)) -> None:
    pass
    #
    # message_to_produce = json.dumps(message.model_dump()).encode(encoding="utf-8")
    # print("OK", message_to_produce)
    # await producer.send(value=message_to_produce)



# Не работает - переделат под FastApi - что бы был еще сервис с моделько изолированный
def start_async_task():
    asyncio.run(get_text())

if __name__ == "__main__":
    start_async_task()