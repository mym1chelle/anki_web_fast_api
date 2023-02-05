from pydantic import BaseModel


class ExtendedModel(BaseModel):

    class Config:
        orm_mode = True


class CreateDeck(BaseModel):
    name: str


class BaseDeck(ExtendedModel):
    name: str
