import uuid
from fastapi import Depends
from typing import Annotated
from sqlmodel import Session

from src.exceptions import ClientNotFoundError, DuplicateEmailError
from src.client.repository import ClientRepository, client_repository
from src.client.schemas import ClientIn, ClientOut
from src.client.models import Client


class ClientUseCases:
    def __init__(self: 'ClientUseCases', repository: ClientRepository) -> None:
        self.repository = repository

    async def create(self: 'ClientUseCases', db: Session, client_in: ClientIn) -> ClientOut:
        # if await self.repository.get_by_email(email=client_in.email):
        #     raise DuplicateEmailError()

        #new_client = await self.repository.create(client=Client(**client_in.model_dump()))
        client_model = Client(**client_in.model_dump())

        new_client = await self.repository.create(db=db, model=client_model)

        return ClientOut(id=new_client.id, **client_in.model_dump())

    # async def get(self: 'UseCases', id: UUID4) -> ClientOut:
    #     client = await self.repository.get_by_id(id=id)

    #     if not client:
    #         raise ClientNotFoundError()

    #     return ClientOut(**client.model_dump())

    # async def update(self: 'UseCases', id: UUID4, client_in: ClientIn) -> ClientOut:
    #     client = await self.get(id=id)

    #     if client_in.email != client.email and await self.repository.get_by_email(email=client_in.email):
    #         raise DuplicateEmailError()

    #     new_client = Client(id=client.id, **client_in.model_dump())

    #     client = await self.repository.update(client=new_client)

    #     return ClientOut(**client.model_dump())

    # async def delete_client(self: 'UseCases', id: UUID4) -> None:
    #     await self.repository.delete(id=id)


async def client_usecase() -> ClientUseCases:
    repository = await client_repository()

    return ClientUseCases(repository=repository)


ClientUseCaseDependency = Annotated[ClientUseCases, Depends(client_usecase)]
