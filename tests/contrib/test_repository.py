import pytest
from sqlalchemy.exc import IntegrityError

from src.contrib.exceptions import UniqueViolation


@pytest.mark.asyncio
async def test_repository_create_with_success(repository, mock_model, mock_async_session) -> None:
    test_model = mock_model()

    result = await repository.create(db=mock_async_session, model=test_model)

    mock_async_session.add.assert_called_once_with(test_model)
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_awaited_once_with(test_model)

    assert result == test_model


@pytest.mark.asyncio
async def test_repository_create_with_unique_violation(repository, mock_model, mock_async_session) -> None:
    test_model = mock_model()
    mock_async_session.commit.side_effect = IntegrityError("", "", "")

    with pytest.raises(UniqueViolation):
        await repository.create(db=mock_async_session, model=test_model)

    mock_async_session.rollback.assert_awaited_once()
