from pydantic import BaseModel
from users.schemas import UserName


class ExtendedModel(BaseModel):
    class Config:
        orm_mode = True


class BaseCard(ExtendedModel):
    question: str
    question_type: int
    answer: str
    answer_type: int


class CreateCard(BaseModel):
    question: str
    question_type: int
    answer: str
    answer_type: int
    style: int
    deck_id: int


class Card(BaseCard):
    style: int
    deck_id: int
    user_id: int


class CardWithCreator(BaseCard):
    created_by: UserName

