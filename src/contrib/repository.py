from datetime import datetime, timezone
from typing import TypeVar
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.contrib.exceptions import NotFoundException, UniqueViolation

ModelType = TypeVar('ModelType')


class RepositoryBase:

    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def create(self: 'RepositoryBase', db: AsyncSession, model: type[ModelType]) -> ModelType:
        try:
            db.add(model)
            await db.commit()
            await db.refresh(model)
        except IntegrityError:
            await db.rollback()
            raise UniqueViolation(f"Unique constraint violated for {model.email}")

        return model

    async def get(self, db: AsyncSession, id: UUID) -> ModelType:
        statement = select(self.model).where(self.model.id == id)
        result = await db.exec(statement)
        result = result.scalar_one_or_none()

        if result is None:
            raise NotFoundException(f"Object with id {id} not found")

        return result

    async def update(self, db: AsyncSession, model_db: ModelType, model: ModelType) -> ModelType:
        update_data = model.model_dump()

        updated = update(self.model).where(self.model.id == model_db.id).values(**update_data)

        result = await db.exec(updated)

        if result.rowcount == 0:
            raise NotFoundException(f"Object with id {model_db.id} not found")

        await db.commit()

        return model

    async def delete(self, db: AsyncSession, id: UUID) -> None:
        updated = (
            update(self.model).where(self.model.id == id).values(is_active=False, deleted_at=datetime.now(timezone.utc))
        )
        result = await db.exec(updated)

        if result.rowcount == 0:
            raise NotFoundException(f"Object with id {id} not found")

        await db.commit()
