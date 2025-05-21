from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID, uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.contrib.repository import RepositoryBase


@pytest.fixture
def mock_model():
    class MockModel:
        def __init__(self, id: UUID = None, email: str = None, is_active: bool = True):
            self.id = id or uuid4()
            self.email = email or "test@example.com"
            self.is_active = is_active

        def model_dump(self):
            return {"email": self.email, "is_active": self.is_active}

    return MockModel


@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.fixture
def repository(mock_model):
    return RepositoryBase(model=mock_model)


@pytest.fixture
def mock_settings():
    with patch('src.contrib.security.settings') as mock:
        mock.SECRET_KEY = 'test-secret-key'
        mock.REDIS_HOST = 'localhost'
        mock.REDIS_PORT = 6379
        yield mock


@pytest.fixture
def mock_datetime():
    with patch('src.contrib.security.datetime') as mock:
        fixed_now = datetime(2028, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock.now.return_value = fixed_now
        yield fixed_now


@pytest.fixture
def mock_redis_client(mocker):
    mock_client = Mock()
    mocker.patch('src.contrib.cache.redis_client', mock_client)
    return mock_client
