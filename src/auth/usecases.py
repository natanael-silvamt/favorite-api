from typing import Annotated

from fastapi import Depends
from pydantic import UUID4
from sqlmodel import Session

from src.auth.exceptions import EmailOrPasswordInvalid, UserInactive, UserNotFound
from src.auth.models import User
from src.auth.repository import AuthRepository, auth_repository
from src.auth.schemas import UserIn, UserOut
from src.contrib.exceptions import NotFoundException
from src.contrib.security import get_password_hash, verify_password


class AuthUseCases:
    def __init__(self: 'AuthUseCases', repository: AuthRepository) -> None:
        self.repository = repository

    async def create_user(self: 'AuthUseCases', db: Session, user_in: UserIn) -> UserOut:
        user_in.hashed_password = get_password_hash(user_in.hashed_password)

        user_model = User(**user_in.model_dump())

        new_user = await self.repository.create(db=db, model=user_model)

        return UserOut(**new_user.model_dump())

    async def get_user(self: 'AuthUseCases', db: Session, id: UUID4) -> UserOut:
        try:
            user = await self.repository.get(db=db, id=id)
        except NotFoundException as ex:
            raise UserNotFound(message=f'User with id {id} not found')

        if not user.is_active:
            raise UserNotFound(message=f'User with id {id} not found')

        return UserOut(**user.model_dump())

    async def autenticate(self: 'AuthUseCases', db: Session, email: str, password: str) -> UserOut:
        try:
            user = await self.repository.get_user_by_email(db=db, email=email)
        except NotFoundException as ex:
            raise UserNotFound(message=f'User with email {email} not found')

        if not user.is_active:
            raise UserInactive(message=f'User with email {email} is inactive')

        if not verify_password(plain_password=password, hashed_password=user.hashed_password):
            raise EmailOrPasswordInvalid()

        return UserOut(**user.model_dump())


async def auth_usecase() -> AuthUseCases:
    repository = await auth_repository()

    return AuthUseCases(repository=repository)


AuthUseCaseDependency = Annotated[AuthUseCases, Depends(auth_usecase)]
