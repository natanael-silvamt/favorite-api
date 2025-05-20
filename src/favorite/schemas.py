from uuid import UUID

from pydantic import BaseModel


class RantingFavorite(BaseModel):
    rate: float
    count: int

class FavoriteOut(BaseModel):
    id: UUID
    client_id: UUID
    product_id: int
    title: str
    image: str
    price: float
    rating: RantingFavorite


class FavoriteIn(BaseModel):
    client_id: UUID
    product_id: int

