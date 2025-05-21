import pytest
from fastapi import status
from httpx import AsyncClient, Response
from pytest_mock import MockerFixture


@pytest.fixture
async def mock_http_request(mocker: MockerFixture):
    return mocker.patch.object(
        AsyncClient,
        'request',
        return_value=Response(
            status_code=status.HTTP_200_OK, headers={'content-type': 'application/json'}, json={'key': 'value'}
        ),
    )
