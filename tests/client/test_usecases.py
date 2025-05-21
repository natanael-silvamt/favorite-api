from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from src.client.exceptions import ClientNotFound, DuplicateEmail
from src.contrib.exceptions import NotFoundException, UniqueViolation


@pytest.mark.asyncio
async def test_usecase_create_client_with_success(
    client_use_cases, mock_repository, mock_db, client_in, client_model, client_out
) -> None:
    mock_repository.create = AsyncMock(return_value=client_model)

    result = await client_use_cases.create(db=mock_db, client_in=client_in)

    assert result.name == client_out.name


@pytest.mark.asyncio
async def test_usecase_create_client_with_duplicate_email(
    client_use_cases, mock_repository, mock_db, client_in
) -> None:
    mock_repository.create = AsyncMock(side_effect=UniqueViolation("Duplicate email"))

    with pytest.raises(DuplicateEmail, match=f"Email {client_in.email} already exists") as exc:
        await client_use_cases.create(db=mock_db, client_in=client_in)

    assert exc.value.message == f"Email {client_in.email} already exists"


@pytest.mark.asyncio
async def test_usecase_get_client_with_success(client_use_cases, mock_repository, mock_db, client_model, client_out):
    client_id = UUID("6069131c-20e6-47de-918e-4cbc02e8ee34")
    client_model.id = client_id

    mock_repository.get = AsyncMock(return_value=client_model)

    result = await client_use_cases.get(db=mock_db, id=client_id)

    mock_repository.get.assert_awaited_once_with(db=mock_db, id=client_id)
    assert result == client_out
