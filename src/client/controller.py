from fastapi import APIRouter, Body, status

from src.client.schemas import ClientIn, ClientOut
from src.client.usecases import ClientUseCaseDependency
from src.database import SessionDependency

router = APIRouter(tags=['clients'])


@router.post(
    '/clients',
    summary='Create an client',
    status_code=status.HTTP_201_CREATED,
    response_model=ClientOut,
)
async def post(
    session: SessionDependency,
    use_case: ClientUseCaseDependency,
    client_in: ClientIn = Body(...),
) -> ClientOut:
    client = await use_case.create(db=session, client_in=client_in)

    return client
