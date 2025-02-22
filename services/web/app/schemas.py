from pydantic import BaseModel


class Message(BaseModel):
    text: str
    user_id: int
    text_id: int


class Prediction(BaseModel):
    text: str
    prediction: float
    user_id: int
    text_id: int