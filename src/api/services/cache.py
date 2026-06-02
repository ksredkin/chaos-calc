import json

from redis.asyncio import Redis

from src.api.redis.client import r
from src.api.utils.logger import Logger

logger = Logger("Cache Serice")


class CacheService:
    def __init__(self, redis: Redis):
        self.r = redis

    async def _get(self, prefix: str, key: str) -> str | bool | None:
        full_key = f"{prefix}:{key}"
        data: str | bool | None = await self.r.get(full_key)  # type: ignore

        if not data:
            logger.info(f"Кэш не найден: {full_key}")
            return None

        logger.info(f"Кэш найден: {full_key}")
        return data

    async def _set(
        self, prefix: str, key: str, value: str, expire: int | None = None
    ) -> None:
        full_key = f"{prefix}:{key}"
        await self.r.set(full_key, value, ex=expire)
        ttl_str = f" (истечет через {expire}с)" if expire else " (без лимита)"
        logger.info(f"Данные сохранены в кэш: {full_key}{ttl_str}")

    async def _del(self, prefix: str, key: str) -> None:
        full_key = f"{prefix}:{key}"
        await self.r.delete(full_key)

    async def set_expression_result(
        self, expr: str, result: dict[str, str | int]
    ) -> None:
        await self._set("expression", expr, json.dumps(result), 86400)

    async def get_expression_result(self, expr: str) -> None | dict[str, str | int]:
        result = await self._get("expression", expr)
        return json.loads(result) if isinstance(result, str) else None


cache = CacheService(r)
