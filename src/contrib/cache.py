import json
from typing import Any, Dict, Optional

import redis

from src.config import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


def get_product_from_cache(product_id: int) -> Optional[Dict[str, Any]]:
    cached_data = redis_client.get(f"produto:{product_id}")
    return json.loads(cached_data) if cached_data else None


def set_product_in_cache(product_id: int, product_data: Dict[str, Any], ttl: int = 3600) -> None:
    redis_client.setex(f"produto:{product_id}", ttl, json.dumps(product_data))
