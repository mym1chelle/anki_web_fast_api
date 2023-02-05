from pydantic import BaseModel


class CreateStyle(BaseModel):
    name: str
