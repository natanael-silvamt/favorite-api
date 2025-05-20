import uuid
from sqlmodel import Session
from sqlalchemy.future import select

from src.contrib.repository import RepositoryBase
from src.favorite.models import Favorite


class FavoriteRepository(RepositoryBase):
    async def exists_by_client_and_product(
        self: 'FavoriteRepository', db: Session, client_id: uuid.UUID, product_id: int
    ) -> bool:
        statemant = select(self.model).where(
            self.model.client_id == client_id,
            self.model.product_id == product_id
        )

        result = await db.exec(statemant)
        result = result.scalar_one_or_none()

        return False if not result else True
    
    async def get_by_client_id(self: 'FavoriteRepository', db: Session, client_id: uuid.UUID) -> list[Favorite]:
        statement = select(self.model).where(
            self.model.client_id == client_id
        )

        result = await db.exec(statement)
        result = result.all()

        return result


async def favorite_repository() -> FavoriteRepository:
    return FavoriteRepository(model=Favorite)
