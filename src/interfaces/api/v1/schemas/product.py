from pydantic import BaseModel
from uuid import UUID
from src.core.entities.product import Favorite


class FavoriteProductOut(BaseModel):
    id: UUID
    client_id: UUID
    product_id: int
    title: str
    image: str
    price: float
    review_score: float | None
    
    @classmethod
    def from_entity(cls, favorite: Favorite) -> "FavoriteProductOut":
        return cls(**favorite.__dict__)
