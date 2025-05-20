from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4

from src.auth.exceptions import EmailOrPasswordInvalid, UserInactive, UserNotFound
from src.auth.schemas import Token, UserIn, UserOut
from src.auth.usecases import AuthUseCaseDependency
from src.config import settings
from src.contrib import security
from src.database import SessionDependency
from src.dependencies import SuperUserDependency

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
async def login_access_token(
    auth_usecase: AuthUseCaseDependency,
    session: SessionDependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    try:
        user = await auth_usecase.autenticate(
            db=session,
            email=form_data.username,
            password=form_data.password,
        )
    except UserNotFound as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message,
        )
    except (UserInactive, EmailOrPasswordInvalid) as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.message,
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(access_token=security.create_access_token(user.id, expires_delta=access_token_expires))


@router.post(
    '/auth/users',
    summary='Create an user',
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
)
async def create_user(
    session: SessionDependency,
    auth_usecase: AuthUseCaseDependency,
    _: SuperUserDependency,
    user_in: UserIn = Body(...),
) -> UserOut:
    user = await auth_usecase.create_user(db=session, user_in=user_in)
    return user


@router.get(
    '/auth/users/{id}',
    summary='Get an user',
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
)
async def get_user(
    session: SessionDependency,
    auth_usecase: AuthUseCaseDependency,
    id: UUID4,
    _: SuperUserDependency,
) -> UserOut:
    try:
        user = await auth_usecase.get_user(session=session, id=id)
    except UserNotFound as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message,
        )

    return user
