from typing import Annotated

from fastapi import Depends
from pydantic import UUID4
from sqlmodel import Session

from src.client.exceptions import ClientNotFound, DuplicateEmail
from src.client.models import Client
from src.client.repository import ClientRepository, client_repository
from src.client.schemas import ClientIn, ClientOut
from src.contrib.exceptions import NotFoundException, UniqueViolation


class ClientUseCases:
    def __init__(self: 'ClientUseCases', repository: ClientRepository) -> None:
        self.repository = repository

    async def create(self: 'ClientUseCases', db: Session, client_in: ClientIn) -> ClientOut:
        client_model = Client(**client_in.model_dump())

        try:
            new_client = await self.repository.create(db=db, model=client_model)
        except UniqueViolation as ex:
            raise DuplicateEmail(f'Email {client_in.email} already exists')

        return ClientOut(id=new_client.id, **client_in.model_dump())

    async def get(self: 'ClientUseCases', db: Session, id: UUID4) -> ClientOut:
        try:
            client = await self.repository.get(db=db, id=id)
        except NotFoundException as ex:
            raise ClientNotFound(message=f'Client with id {id} not found')

        if not client.is_active:
            raise ClientNotFound(message=f'Client with id {id} not found')

        return ClientOut(**client.model_dump())

    async def get_by_email(self: 'ClientUseCases', db: Session, email: str) -> ClientOut:
        try:
            client = await self.repository.get_by_email(db=db, email=email)
        except NotFoundException as ex:
            raise ClientNotFound(message=f'Client with email {email} not found')

        if not client.is_active:
            raise ClientNotFound(message=f'Client with email {email} not found')

        return ClientOut(**client.model_dump())

    async def update(self: 'ClientUseCases', db: Session, id: UUID4, client_in: ClientIn) -> ClientOut:
        client = await self.get(db=db, id=id)

        if client_in.email != client.email and await self.repository.get_by_email(email=client_in.email):
            raise DuplicateEmail(f'Email {client_in.email} already exists')

        new_client = Client(id=client.id, **client_in.model_dump())

        client_updated = await self.repository.update(db=db, model_db=client, model=new_client)

        return ClientOut(**client_updated.model_dump())

    async def delete(self: 'ClientUseCases', db: Session, id: UUID4) -> None:
        try:
            await self.repository.delete(db=db, id=id)
        except NotFoundException as ex:
            raise ClientNotFound(message=f'Client with id {id} not found')


async def client_usecase() -> ClientUseCases:
    repository = await client_repository()

    return ClientUseCases(repository=repository)


ClientUseCaseDependency = Annotated[ClientUseCases, Depends(client_usecase)]
