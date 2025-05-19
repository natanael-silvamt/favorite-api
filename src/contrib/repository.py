from typing import TypeVar, Generic, Optional
from uuid import UUID
from sqlmodel import Session
from sqlalchemy.future import select
from sqlalchemy import update, delete

ModelType = TypeVar('ModelType')


class RepositoryBase:
    async def create(self: 'RepositoryBase', db: Session, model: type[ModelType]) -> ModelType:
        db.add(model)
        await db.commit()
        await db.refresh(model)

        return model

    # async def get(self, db: AsyncSession, id: UUID) -> Optional[ModelType]:
    #     result = await db.execute(
    #         select(self.model).where(self.model.id == id)  # type: ignore
    #     return result.scalars().first()

    # async def get_multi(
    #     self, 
    #     db: AsyncSession, 
    #     *, 
    #     skip: int = 0, 
    #     limit: int = 100
    # ) -> List[ModelType]:
    #     result = await db.execute(
    #         select(self.model).offset(skip).limit(limit))  # type: ignore
    #     return result.scalars().all()

    # async def update(
    #     self, 
    #     db: AsyncSession, 
    #     *, 
    #     db_obj: ModelType, 
    #     obj_in: PydanticModel
    # ) -> ModelType:
    #     update_data = obj_in.dict(exclude_unset=True)
    #     await db.execute(
    #         update(self.model)
    #         .where(self.model.id == db_obj.id)  # type: ignore
    #         .values(**update_data)
    #     )
    #     await db.commit()
    #     await db.refresh(db_obj)
    #     return db_obj

    # async def delete(self, db: AsyncSession, *, id: UUID) -> None:
    #     await db.execute(
    #         delete(self.model).where(self.model.id == id))  # type: ignore
    #     )
    #     await db.commit()