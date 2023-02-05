from pydantic import BaseModel


class CreateType(BaseModel):
    name: str
