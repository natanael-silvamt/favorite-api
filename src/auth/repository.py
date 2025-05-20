from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.models import User
from src.contrib.exceptions import NotFoundException
from src.contrib.repository import RepositoryBase


class AuthRepository(RepositoryBase):

    async def get_user_by_email(self: 'AuthRepository', db: AsyncSession, email: str) -> User:
        statement = select(self.model).where(self.model.email == email)
        result = await db.exec(statement)
        result = result.scalar_one_or_none()

        if result is None:
            raise NotFoundException(f"User with email {email} not found")

        return result


async def auth_repository() -> AuthRepository:
    return AuthRepository(model=User)
