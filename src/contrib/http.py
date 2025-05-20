import functools
import json
import time
from http import HTTPStatus
from typing import Any

import httpx
from pydantic import BaseModel, AnyUrl

from src.contrib.schemas import Config, Method, Response
from src.contrib.exceptions import RequestError


class Client:
    config: Config = Config()

    TIMEOUT = 5

    def __init__(self: 'Client', *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.client = httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=self.config.max_connections,
                max_keepalive_connections=self.config.max_connections,
            )
        )

    async def _request(
        self: 'Client',
        method: Method,
        endpoint: AnyUrl,
        data: BaseModel | None = None,
        timeout: float | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        headers = headers or {}

        headers.update({'Content-Type': 'application/json'})

        retry_attempts = self.config.retry_attempts

        if retry_attempts <= 0:
            raise RequestError(message='Retry attempts has an invalid value')

        response = await self._process(
            retry_attempts=retry_attempts, method=method, endpoint=endpoint, data=data, timeout=timeout, headers=headers
        )

        return self._parse_response(response)

    async def _process(
        self: 'Client',
        retry_attempts: int,
        method: Method,
        endpoint: AnyUrl,
        data: BaseModel | None,
        timeout: float | None,
        headers: dict[str, str],
    ) -> httpx.Response:
        response: httpx.Response

        while retry_attempts:
            start: float = time.time()

            try:
                response = await self.client.request(
                    method=method,
                    url=endpoint,
                    json=json.loads(data.model_dump_json()) if data else None,
                    data=data.model_dump_json().encode('utf-8') if data else None,
                    headers=headers,
                    timeout=timeout or self.TIMEOUT,
                )

                duration = '{0:.3f}s'.format(time.time() - start)

                await response.aclose()

                return response
            except RequestError:
                raise
            except httpx.TimeoutException:
                retry_attempts = self._process_attempts(endpoint=endpoint, attempts=retry_attempts, start=start)
            except Exception as exc:
                duration = '{0:.3f}s'.format(time.time() - start)

                raise RequestError(
                    message=f'An error occurred with duration: {duration} url: {endpoint} and error: {exc}'
                )

        return response

    def _process_attempts(self: 'Client', endpoint: AnyUrl, attempts: int, start: float) -> int:
        attempts -= 1

        if not attempts:
            duration = '{0:.3f}s'.format(time.time() - start)

            raise RequestError(
                message=f'Timeout error with duration: {duration} url: {endpoint}',
                status_code=HTTPStatus.GATEWAY_TIMEOUT,
            )

        return attempts

    def _parse_response(self: 'Client', response: httpx.Response) -> Response:
        try:
            content = response.json()
        except json.JSONDecodeError:
            content = None

        return Response(
            content=content,
            status_code=response.status_code,
        )

    get = functools.partialmethod(_request, Method.get)
