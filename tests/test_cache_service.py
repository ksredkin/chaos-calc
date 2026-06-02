import os

os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"

import pytest
from fakeredis.aioredis import FakeRedis


@pytest.mark.asyncio
async def test_cache_service(redis: FakeRedis) -> None:
    from src.api.services.cache import CacheService

    cache = CacheService(redis)

    expr = "2+2"
    result: dict[str, str | int] = {"expression": expr, "result": "4", "total_votes": 1}

    assert await cache.get_expression_result(expr) is None

    await cache.set_expression_result(expr, result)

    cached_result = await cache.get_expression_result(expr)
    assert cached_result == result
