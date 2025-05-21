from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.contrib.http import Client as HttpClient
from src.favorite.models import Favorite
from src.favorite.repository import FavoriteRepository
from src.favorite.schemas import FavoriteIn, FavoriteOut, RantingFavorite
from src.favorite.usecases import FavoriteUseCases


@pytest.fixture
def mock_repository():
    return MagicMock(spec=FavoriteRepository)


@pytest.fixture
def mock_http_client():
    return MagicMock(spec=HttpClient)


@pytest.fixture
def favorite_use_cases(mock_repository, mock_http_client):
    use_case = FavoriteUseCases(repository=mock_repository)
    use_case.client = mock_http_client
    return use_case


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def favorite_in():
    return FavoriteIn(client_id=UUID("6069131c-20e6-47de-918e-4cbc02e8ee34"), product_id=1)


@pytest.fixture
def favorite_model(favorite_in):
    return Favorite(id=UUID("6069131c-20e6-47de-918e-4cbc02e8ee34"), **favorite_in.model_dump())


@pytest.fixture
def product_data():
    return {
        "title": "Test Product",
        "image": "http://example.com/image.jpg",
        "price": 99.99,
        "rating": {"rate": 4.5, "count": 100},
    }


@pytest.fixture
def favorite_out(favorite_model, product_data):
    return FavoriteOut(
        **favorite_model.model_dump(),
        title=product_data["title"],
        image=product_data["image"],
        price=product_data["price"],
        rating=RantingFavorite(**product_data["rating"]),
    )
