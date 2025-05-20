from datetime import datetime

from pydantic import UUID4, BaseModel, validator


class ClientIn(BaseModel):
    name: str
    email: str


class ClientOut(BaseModel):
    id: UUID4
    name: str
    email: str
    created_at: str
    updated_at: str

    @validator('created_at', 'updated_at', pre=True)
    def convert_datetime_to_str(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value
