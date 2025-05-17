from pydantic import UUID4

from src.core.entities.client import Client
from src.core.exceptions import ClientNotFoundError, DuplicateEmailError
from src.core.repositories.client import ClientRepository
from src.interfaces.api.v1.schemas.client import ClientIn, ClientOut


class UseCases:
    def __init__(self: 'UseCases', repository: ClientRepository) -> None:
        self.repository = repository

    async def create(self: 'UseCases', client_in: ClientIn) -> ClientOut:
        if await self.repository.get_by_email(email=client_in.email):
            raise DuplicateEmailError()

        new_client = await self.repository.create(client=Client(**client_in.model_dump()))

        return ClientOut(**new_client.model_dump())

    async def get(self: 'UseCases', id: UUID4) -> ClientOut:
        client = await self.repository.get_by_id(id=id)

        if not client:
            raise ClientNotFoundError()

        return ClientOut(**client.model_dump())

    # async def update(self: 'UseCases', id: UUID4, client_in: ClientIn) -> ClientOut:
    #     client = await self.get(id=id)

    #     if client_in.email != client.email and await self.repository.get_by_email(email=client_in.email):
    #         raise DuplicateEmailError()

    #     new_client = Client(id=client.id, **client_in.model_dump())

    #     client = await self.repository.update(client=new_client)

    #     return ClientOut(**client.model_dump())

    async def delete_client(self: 'UseCases', id: UUID4) -> None:
        await self.repository.delete(id=id)
