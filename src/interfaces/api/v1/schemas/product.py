from pydantic import BaseModel
from uuid import UUID


class FavoriteProductOut(BaseModel):
    id: UUID
    client_id: UUID
    product_id: int
    title: str
    image: str
    price: float
    review_score: float | None
