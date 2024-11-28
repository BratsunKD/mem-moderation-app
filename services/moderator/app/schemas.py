from pydantic import BaseModel


class Message(BaseModel):
    text: str
    user_id: int


class ModelPredict(BaseModel):
    text: str
    user_id: int
    model_predict: str
