from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.client.models import Client
from src.contrib.exceptions import NotFoundException
from src.contrib.repository import RepositoryBase


class ClientRepository(RepositoryBase):

    async def get_by_email(self: 'ClientRepository', db: AsyncSession, email: str) -> Client:
        statement = select(self.model).where(self.model.email == email)
        result = await db.exec(statement)
        result = result.scalar_one_or_none()

        if result is None:
            raise NotFoundException(f"Client with email {email} not found")

        return result


async def client_repository() -> ClientRepository:
    return ClientRepository(model=Client)
