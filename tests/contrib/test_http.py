from http import HTTPStatus

import httpx
import pytest

from src.contrib.exceptions import RequestError
from src.contrib.http import Client as ClientHttp
from src.contrib.schemas import Config as ConfigHttp


class FakeHttpClient(ClientHttp):
    config = ConfigHttp(max_connections=1, retry_attempts=2)


@pytest.fixture
def http_client():
    return FakeHttpClient()


def test_http_client_should_have_only_one_instance() -> None:
    http_client_one = FakeHttpClient()
    http_client_two = FakeHttpClient()

    assert http_client_one == http_client_two


@pytest.mark.usefixtures('mock_http_request')
async def test_get_should_return_ok(http_client) -> None:
    response = await http_client.get('https://fakestoreapi.com/products/1')

    assert response.content == {'key': 'value'}
    assert response.status_code == HTTPStatus.OK


async def test_get_no_content_should_return_ok(http_client, mock_http_request) -> None:
    mock_http_request.return_value.json = lambda: ''
    mock_http_request.return_value.status_code = HTTPStatus.NO_CONTENT

    response = await http_client.get('https://fakestoreapi.com/products/0')

    assert not response.content
    assert response.status_code == HTTPStatus.NO_CONTENT


async def test_get_should_raise_for_timeout(http_client, mock_http_request) -> None:
    with pytest.raises(RequestError) as exc:
        mock_http_request.side_effect = httpx.TimeoutException(message='TimeoutError')
        await http_client.get('https://fakestoreapi.com/products/1')

    assert 'Timeout error' in exc.value.message


@pytest.mark.parametrize(
    'retry_attempts',
    [0, -1],
)
async def test_get_should_return_none_if_no_retry_attempts(http_client, mock_http_request, retry_attempts) -> None:
    http_client.config.retry_attempts = retry_attempts

    with pytest.raises(RequestError) as exc:
        await http_client.get('https://fakestoreapi.com/products/1')

    assert exc.value.message == 'Retry attempts has an invalid value'
