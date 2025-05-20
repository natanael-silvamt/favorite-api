from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class RantingFavorite(BaseModel):
    rate: float
    count: int


class FavoriteOut(BaseModel):
    id: UUID
    client_id: UUID
    product_id: int
    created_at: str
    title: str
    image: str
    price: float
    rating: RantingFavorite

    @validator('created_at', pre=True)
    def convert_datetime_to_str(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value


class FavoriteIn(BaseModel):
    client_id: UUID
    product_id: int
