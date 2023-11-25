import datetime
from pydantic import BaseModel, Field


class ConsultationIn(BaseModel):
    client_id: int = Field(..., title="client_id")
    pet_id: int = Field(..., title="pet_id")
    date_time: datetime.datetime = Field(..., title="date_time")
    description: str = Field(default='', title="description", max_length=300)


class Consultation(ConsultationIn):
    id: int
