from datetime import timedelta
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response
from pytest_mock import MockerFixture

from src.contrib.security import create_access_token
from src.dependencies import CurrentUserDependency
from src.routers import api_router


@pytest.fixture
async def mock_http_request(mocker: MockerFixture):
    return mocker.patch.object(
        AsyncClient,
        'request',
        return_value=Response(
            status_code=status.HTTP_200_OK, headers={'content-type': 'application/json'}, json={'key': 'value'}
        ),
    )


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    return app


@pytest.fixture
def mock_current_user():
    mock_user = AsyncMock()
    mock_user.id = "user123"
    mock_user.email = "test@example.com"
    mock_user.is_active = True

    return mock_user


@pytest.fixture
async def client(app: FastAPI, mock_current_user) -> AsyncGenerator:
    app.dependency_overrides[CurrentUserDependency] = mock_current_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    # return TestClient(app)
    # async with AsyncClient(app=app, base_url='http://favorite.com') as ac:
    #     yield ac


@pytest.fixture
def auth_token():
    return create_access_token(subject="test-user", expires_delta=timedelta(minutes=30))


@pytest.fixture
def headers(auth_token: str) -> dict:
    return {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
