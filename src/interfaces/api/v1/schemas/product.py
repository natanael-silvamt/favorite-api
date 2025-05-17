from uuid import UUID

from pydantic import BaseModel


class FavoriteProductOut(BaseModel):
    id: UUID
    client_id: UUID
    product_id: int
    title: str
    image: str
    price: float
    review_score: float | None
