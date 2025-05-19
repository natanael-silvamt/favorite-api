from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.healthchecks.schemas import HealthCheckOut

router = APIRouter(tags=['healthchecks'])


@router.head(
    '/ping',
    status_code=HTTPStatus.OK,
    response_model=HealthCheckOut,
)
@router.get(
    '/ping',
    status_code=HTTPStatus.OK,
    response_model=HealthCheckOut,
)
async def ping() -> JSONResponse:
    return JSONResponse(content='pong', status_code=HTTPStatus.OK)
