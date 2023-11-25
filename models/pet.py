import datetime
from pydantic import BaseModel, Field


class PetIn(BaseModel):
    client_id: int = Field(..., title="client_id")
    name: str = Field(..., title="name", max_length=80)
    birthday: datetime.date = Field(..., title="birthday")


class Pet(PetIn):
    id: int
