from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.interfaces.api.v1.schemas.healthchecks import HealthCheckResponse

router = APIRouter(tags=['healthchecks'])


@router.head(
    '/ping',
    status_code=HTTPStatus.OK,
    response_model=HealthCheckResponse,
)
@router.get(
    '/ping',
    status_code=HTTPStatus.OK,
    response_model=HealthCheckResponse,
)
async def ping() -> JSONResponse:
    return JSONResponse(content='pong', status_code=HTTPStatus.OK)
