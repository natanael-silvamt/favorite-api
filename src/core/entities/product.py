from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Favorite(BaseModel):
    id: UUID
    client_id: UUID
    product_id: int
    title: str
    image: str
    price: float
    review_score: Optional[float] = None
