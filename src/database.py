from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=False, future=True)


async def init_db():
    async with engine.begin() as conn:
        pass
        # await conn.run_sync(SQLModel.metadata.drop_all)
        # await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]
