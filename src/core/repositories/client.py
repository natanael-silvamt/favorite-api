from abc import ABC, abstractmethod

from pydantic import UUID4

from src.core.entities.client import Client


class ClientRepository(ABC):
    @abstractmethod
    async def create(self: 'ClientRepository', client: Client) -> Client:
        pass

    @abstractmethod
    async def get_by_id(self: 'ClientRepository', id: UUID4) -> Client | None:
        pass

    @abstractmethod
    async def get_by_email(self: 'ClientRepository', email: str) -> Client | None:
        pass

    @abstractmethod
    async def update(self: 'ClientRepository', client: Client) -> Client:
        pass

    @abstractmethod
    async def delete(self: 'ClientRepository', id: UUID4) -> None:
        pass
