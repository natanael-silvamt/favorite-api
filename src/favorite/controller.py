from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException
from pydantic import UUID4

from src.database import SessionDependency
from src.favorite.exceptions import FavoriteAlreadyExists, FavoriteNotFound
from src.favorite.schemas import FavoriteIn, FavoriteOut
from src.favorite.usecases import FavoriteUseCaseDependency

router = APIRouter(tags=['favorites'])


@router.post(
    '/favorites',
    summary='Create an Favorite',
    status_code=status.HTTP_201_CREATED,
    response_model=FavoriteOut,
)
async def post(
    session: SessionDependency,
    use_case: FavoriteUseCaseDependency,
    favorite_in: FavoriteIn = Body(...),
) -> FavoriteOut:
    try:
        favorite = await use_case.create(db=session, favorite_in=favorite_in)
    except FavoriteAlreadyExists as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)

    return favorite


@router.get(
    '/favorites/{id}',
    summary='Get favorite by id',
    status_code=status.HTTP_200_OK,
    response_model=FavoriteOut,
)
async def get(
    session: SessionDependency,
    use_case: FavoriteUseCaseDependency,
    id: UUID4,
) -> FavoriteOut:
    try:
        favorite = await use_case.get(db=session, id=id)
    except FavoriteNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)

    return favorite


@router.get(
    '/favorites/clients/{client_id}',
    summary='Get favorite by client_id',
    status_code=status.HTTP_200_OK,
    response_model=list[FavoriteOut],
)
async def get_by_client_id(
    session: SessionDependency,
    use_case: FavoriteUseCaseDependency,
    client_id: UUID4,
) -> list[FavoriteOut] | list:
    favorites = await use_case.get_by_client_id(db=session, client_id=client_id)

    return favorites


@router.delete(
    '/favorites/{id}',
    summary='Delete favorite by id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    session: SessionDependency,
    use_case: FavoriteUseCaseDependency,
    id: UUID4,
) -> None:
    try:
        await use_case.delete(db=session, id=id)
    except FavoriteNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.delete(
    '/favorites/{product_id}/clients/{client_id}',
    summary='Delete favorite by client_id and product_id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_by_client_and_product(
    session: SessionDependency,
    use_case: FavoriteUseCaseDependency,
    product_id: int,
    client_id: UUID4,
) -> None:
    try:
        await use_case.delete_by_client_and_product(db=session, client_id=client_id, product_id=product_id)
    except FavoriteNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
