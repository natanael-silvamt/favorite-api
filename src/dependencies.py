from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from src.auth.models import User
from src.config import settings
from src.contrib import security
from src.database import SessionDependency

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_BASE_URL}/login/access-token")

TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(session: SessionDependency, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
    except (InvalidTokenError, ValidationError) as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = await session.get(User, payload["sub"])

    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUserDependency) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user


SuperUserDependency = Annotated[User, Depends(get_current_active_superuser)]
