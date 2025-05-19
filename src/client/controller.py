from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException
from pydantic import UUID4

from src.client.exceptions import ClientNotFound, DuplicateEmail
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
    try:
        client = await use_case.create(db=session, client_in=client_in)
    except DuplicateEmail as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)

    return client


@router.get(
    '/clients/{id}',
    summary='Get a Client by id',
    status_code=status.HTTP_200_OK,
)
async def get(
    session: SessionDependency,
    id: UUID4,
    use_case: ClientUseCaseDependency,
) -> ClientOut:
    try:
        return await use_case.get(db=session, id=id)
    except ClientNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(
    '/clients/email/{email}',
    summary='Get a Client by email',
    status_code=status.HTTP_200_OK,
)
async def get_by_email(
    session: SessionDependency,
    email: str,
    use_case: ClientUseCaseDependency,
) -> ClientOut:
    try:
        return await use_case.get_by_email(db=session, email=email)
    except ClientNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.put(
    '/clients/{id}',
    summary='Update a Client by id',
    status_code=status.HTTP_200_OK,
    response_model=ClientOut,
)
async def put(
    session: SessionDependency,
    id: UUID4,
    use_case: ClientUseCaseDependency,
    client_in: ClientIn = Body(...),
) -> ClientOut:
    try:
        return await use_case.update(db=session, id=id, client_in=client_in)
    except ClientNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except DuplicateEmail as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.delete(
    '/clients/{id}',
    summary='Delete a Client by id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    session: SessionDependency,
    id: UUID4,
    use_case: ClientUseCaseDependency,
) -> None:
    try:
        await use_case.delete(db=session, id=id)
    except ClientNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
