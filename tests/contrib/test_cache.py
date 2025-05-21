import json

import pytest

from src.contrib.cache import get_product_from_cache, set_product_in_cache


def test_cache_get_product_from_cache_with_success(mock_redis_client) -> None:
    product_id = 1
    expected_data = {"id": 1, "name": "Product 1"}
    mock_redis_client.get.return_value = json.dumps(expected_data)

    result = get_product_from_cache(product_id=product_id)

    mock_redis_client.get.assert_called_once_with(f"produto:{product_id}")
    assert result == expected_data


def test_cache_get_product_from_cache_miss(mock_redis_client) -> None:
    product_id = 99
    mock_redis_client.get.return_value = None

    result = get_product_from_cache(product_id=product_id)

    mock_redis_client.get.assert_called_once_with(f"produto:{product_id}")
    assert result is None


def test_cache_get_product_from_cache_with_invalid_json(mock_redis_client) -> None:
    product_id = 1
    mock_redis_client.get.return_value = "{invalid: json}"

    with pytest.raises(json.JSONDecodeError) as exc:
        get_product_from_cache(product_id=product_id)

    assert str(exc.value) == "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"


def test_cache_set_product_in_cache_with_success(mock_redis_client) -> None:
    product_id = 1
    product_data = {"id": 1, "name": "Product 1"}
    ttl = 3600

    set_product_in_cache(product_id=product_id, product_data=product_data, ttl=ttl)

    mock_redis_client.setex.assert_called_once_with(f"produto:{product_id}", ttl, json.dumps(product_data))
