from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.models import User
from src.config import settings
from src.contrib.security import get_password_hash

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=False, future=True)


async def init_db():
    async with engine.begin() as session:
        existing_user = await session.execute(select(User).where(User.email == settings.FIRST_SUPERUSER))

        existing_user = existing_user.first()

        if existing_user:
            return

        super_user = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )

        await session.execute(insert(User).values(**super_user.model_dump()))
        await session.commit()


async def get_session() -> AsyncGenerator:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]
