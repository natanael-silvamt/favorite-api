from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest


@pytest.mark.asyncio
async def test_usecase_create_user_with_success(
    auth_use_cases, mock_repository, mock_db, user_in, user_model, user_out
) -> None:
    mock_repository.create = AsyncMock(return_value=user_model)

    result = await auth_use_cases.create_user(db=mock_db, user_in=user_in)

    assert result.email == user_out.email
    assert user_in.hashed_password != "plainpassword"


@pytest.mark.asyncio
async def test_usecase_get_user_with_success(auth_use_cases, mock_repository, mock_db, user_model, user_out) -> None:
    user_id = UUID("6069131c-20e6-47de-918e-4cbc02e8ee34")
    mock_repository.get = AsyncMock(return_value=user_model)

    result = await auth_use_cases.get_user(db=mock_db, id=user_id)

    mock_repository.get.assert_awaited_once_with(db=mock_db, id=user_id)
    assert result.email == user_out.email


@pytest.mark.asyncio
async def test_usecase_authenticate_with_success(
    auth_use_cases, mock_repository, mock_db, user_model, user_out
) -> None:
    email = "john@gmail.com"
    password = "12345"

    mock_repository.get_user_by_email = AsyncMock(return_value=user_model)

    with patch('src.auth.usecases.verify_password', return_value=True) as mock_verify:
        result = await auth_use_cases.autenticate(db=mock_db, email=email, password=password)

        mock_repository.get_user_by_email.assert_awaited_once_with(db=mock_db, email=email)
        mock_verify.assert_called_once_with(plain_password=password, hashed_password=user_model.hashed_password)
        assert result.email == user_out.email
