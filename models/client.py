import datetime
from pydantic import BaseModel, Field, field_validator


class ClientIn(BaseModel):
    document: str = Field(..., title="document", min_length=10, max_length=300)
    lastname: str = Field(..., title="lastname", max_length=80)
    firstname: str = Field(..., title="firstname", max_length=80)
    midname: str = Field(..., title="midname", max_length=80)
    birthday: datetime.date = Field(..., title="birthday")


class Client(ClientIn):
    id: int

    @field_validator("birthday")
    def validate_age(cls, value):
        today = datetime.date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if not 18 <= age <= 100:
            raise ValueError("Age must be between 18 and 100.")
        return value
