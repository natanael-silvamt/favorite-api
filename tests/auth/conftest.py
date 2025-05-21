from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.auth.models import User
from src.auth.repository import AuthRepository
from src.auth.schemas import UserIn, UserOut
from src.auth.usecases import AuthUseCases
from tests.auth.factories import user_in_data, user_out_data


@pytest.fixture
def mock_repository():
    return MagicMock(spec=AuthRepository)


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def auth_use_cases(mock_repository):
    return AuthUseCases(repository=mock_repository)


@pytest.fixture
def user_in():
    return UserIn(**user_in_data())


@pytest.fixture
def user_model(user_in):
    return User(
        id=UUID("6069131c-20e6-47de-918e-4cbc02e8ee34"),
        **user_in.model_dump(),
    )


@pytest.fixture
def user_out():
    return UserOut(**user_out_data())
