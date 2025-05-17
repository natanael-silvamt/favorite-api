from abc import ABC, abstractmethod

from pydantic import UUID4

from src.core.entities.product import Favorite


class ProductRepository(ABC):
    @abstractmethod
    async def add_favorite(self: 'ProductRepository', favorite: Favorite) -> Favorite:
        pass

    @abstractmethod
    async def get_favorites(self: 'ProductRepository', client_id: UUID4) -> list[Favorite]:
        pass

    @abstractmethod
    async def remove_favorite(self: 'ProductRepository', client_id: UUID4, product_id: int) -> None:
        pass

    @abstractmethod
    async def is_product_favorited(self: 'ProductRepository', client_id: UUID4, product_id: int) -> bool:
        pass
