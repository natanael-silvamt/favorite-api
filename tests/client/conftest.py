from unittest.mock import MagicMock

import pytest

from src.client.models import Client
from src.client.repository import ClientRepository
from src.client.schemas import ClientIn, ClientOut
from src.client.usecases import ClientUseCases
from tests.client.factories import client_in_data, client_out_data


@pytest.fixture
def client_out():
    return ClientOut(**client_out_data())


@pytest.fixture
def mock_repository():
    return MagicMock(spec=ClientRepository)


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def client_use_cases(mock_repository):
    return ClientUseCases(repository=mock_repository)


@pytest.fixture
def client_in():
    return ClientIn(**client_in_data())


@pytest.fixture
def client_model(client_in):
    return Client(
        **client_in.model_dump(),
        id='6069131c-20e6-47de-918e-4cbc02e8ee34',
        created_at='2023-10-01T12:00:00Z',
        updated_at='2023-10-01T12:00:00Z',
    )
