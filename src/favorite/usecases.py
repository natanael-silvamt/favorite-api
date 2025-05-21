from typing import Annotated, Any

from fastapi import Depends
from pydantic import UUID4
from sqlmodel import Session

from src.config import settings
from src.contrib.cache import get_product_from_cache, set_product_in_cache
from src.contrib.exceptions import NotFoundException, UniqueViolation
from src.contrib.http import Client as HttpClient
from src.contrib.schemas import Config as HttpConfig
from src.favorite.exceptions import FavoriteAlreadyExists, FavoriteNotFound
from src.favorite.models import Favorite
from src.favorite.repository import FavoriteRepository, favorite_repository
from src.favorite.schemas import FavoriteIn, FavoriteOut, RantingFavorite


class FavoriteUseCases:
    def __init__(self: 'FavoriteUseCases', repository: FavoriteRepository) -> None:
        self.repository = repository
        self.client = HttpClient()
        self.client.config = HttpConfig(retry_attempts=settings.RETRY_ATTEMPTS)

    async def create(self: 'FavoriteUseCases', db: Session, favorite_in: FavoriteIn) -> FavoriteOut:
        if await self.repository.exists_by_client_and_product(
            db=db, client_id=favorite_in.client_id, product_id=favorite_in.product_id
        ):
            raise FavoriteAlreadyExists(
                f'Favorite with client_id {favorite_in.client_id} and product_id {favorite_in.product_id} already exists'
            )

        product = await self._get_product(product_id=favorite_in.product_id)

        favorite_model = Favorite(client_id=favorite_in.client_id, product_id=favorite_in.product_id)

        try:
            await self.repository.create(db=db, model=favorite_model)
        except UniqueViolation as ex:
            raise FavoriteAlreadyExists(
                f'Favorite with client_id {favorite_in.client_id} and product_id {favorite_in.product_id} already exists'
            )

        favorite_out = FavoriteOut(
            **favorite_model.model_dump(),
            title=product.get('title'),
            image=product.get('image'),
            price=product.get('price'),
            rating=RantingFavorite(**product.get('rating')),
        )

        return favorite_out

    async def get(self: 'FavoriteUseCases', db: Session, id: UUID4) -> FavoriteOut:
        try:
            favorite = await self.repository.get(db=db, id=id)
        except NotFoundException:
            raise FavoriteNotFound(f'Favorite with id {id} not found')

        product = await self._get_product(product_id=favorite.product_id)

        favorite_out = FavoriteOut(
            **favorite.model_dump(),
            title=product.get('title'),
            image=product.get('image'),
            price=product.get('price'),
            rating=RantingFavorite(**product.get('rating')),
        )

        return favorite_out

    async def get_by_client_id(
        self: 'FavoriteUseCases', db: Session, client_id: UUID4, limit: int, skip: int
    ) -> list[FavoriteOut]:
        favorites = await self.repository.get_by_client_id(db=db, client_id=client_id, limit=limit, skip=skip)

        if not favorites:
            return []

        result = []

        for favorite in favorites:
            favorite = favorite[0]

            product = await self._get_product(product_id=favorite.product_id)

            favorite_out = FavoriteOut(
                **favorite.model_dump(),
                title=product.get('title'),
                image=product.get('image'),
                price=product.get('price'),
                rating=RantingFavorite(**product.get('rating')),
            )

            result.append(favorite_out)

        return result

    async def delete(self: 'FavoriteUseCases', db: Session, id: UUID4) -> None:
        try:
            await self.repository.delete(db=db, id=id)
        except NotFoundException:
            raise FavoriteNotFound(f'Favorite with id {id} not found')

    async def delete_by_client_and_product(
        self: 'FavoriteUseCases', db: Session, client_id: UUID4, product_id: int
    ) -> None:
        try:
            await self.repository.delete_by_client_and_product(db=db, client_id=client_id, product_id=product_id)
        except NotFoundException:
            raise FavoriteNotFound(f'Favorite with client_id {client_id} and product_id {product_id} not found')

    async def _get_product(self: 'FavoriteUseCases', product_id: int) -> dict[str, Any]:
        product = get_product_from_cache(product_id=product_id)

        if not product:
            endpoint = f'{settings.BASE_URL_PRODUCTS}/{product_id}'
            response = await self.client.get(endpoint=endpoint)
            product = response.content

            if not product:
                raise NotFoundException(f'Product with id {product_id} not found')

            set_product_in_cache(product_id=product_id, product_data=product)

        return product


async def favorite_usecase() -> FavoriteUseCases:
    repository = await favorite_repository()

    return FavoriteUseCases(repository=repository)


FavoriteUseCaseDependency = Annotated[FavoriteUseCases, Depends(favorite_usecase)]
