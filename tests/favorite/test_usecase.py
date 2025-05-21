from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest

from src.config import settings


@pytest.mark.asyncio
async def test_usecase_create_with_success(
    favorite_use_cases, mock_repository, mock_db, favorite_in, product_data
) -> None:
    mock_repository.exists_by_client_and_product = AsyncMock(return_value=False)
    mock_repository.create = AsyncMock()

    with (
        patch('src.favorite.usecases.get_product_from_cache', return_value=None),
        patch('src.favorite.usecases.set_product_in_cache'),
        patch.object(favorite_use_cases.client, 'get', return_value=MagicMock(content=product_data)),
    ):

        result = await favorite_use_cases.create(db=mock_db, favorite_in=favorite_in)

        mock_repository.exists_by_client_and_product.assert_awaited_once_with(
            db=mock_db, client_id=favorite_in.client_id, product_id=favorite_in.product_id
        )
        favorite_use_cases.client.get.assert_called_once_with(
            endpoint=f'{settings.BASE_URL_PRODUCTS}/{favorite_in.product_id}'
        )


@pytest.mark.asyncio
async def test_usecase_get_with_success(
    favorite_use_cases, mock_repository, mock_db, favorite_model, product_data
) -> None:
    favorite_id = UUID("6069131c-20e6-47de-918e-4cbc02e8ee34")

    mock_repository.get = AsyncMock(return_value=favorite_model)

    with patch('src.favorite.usecases.get_product_from_cache', return_value=product_data):
        result = await favorite_use_cases.get(db=mock_db, id=favorite_id)

        mock_repository.get.assert_awaited_once_with(db=mock_db, id=favorite_id)



@pytest.mark.asyncio
async def test_usecase_get_by_client_id_with_success(favorite_use_cases, mock_repository, mock_db, favorite_model, product_data, favorite_out) -> None:
    client_id = UUID("6069131c-20e6-47de-918e-4cbc02e8ee34")
    limit = 10
    skip = 1
    
    mock_repository.get_by_client_id = AsyncMock(return_value=[(favorite_model,)])
    
    with patch('src.favorite.usecases.get_product_from_cache', return_value=product_data):
        result = await favorite_use_cases.get_by_client_id(
            db=mock_db, client_id=client_id, limit=limit, skip=skip
        )
        
        mock_repository.get_by_client_id.assert_awaited_once_with(
            db=mock_db, client_id=client_id, limit=limit, skip=skip
        )
        assert len(result) == 1


@pytest.mark.asyncio
async def test_usecase_delete_with_success(favorite_use_cases, mock_repository, mock_db) -> None:
    favorite_id = UUID("6069131c-20e6-47de-918e-4cbc02e8ee34")
    
    mock_repository.delete = AsyncMock()
    
    await favorite_use_cases.delete(db=mock_db, id=favorite_id)
    
    mock_repository.delete.assert_awaited_once_with(db=mock_db, id=favorite_id)
