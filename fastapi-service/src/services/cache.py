from abc import ABC, abstractmethod

from pydantic import BaseModel
from redis.asyncio import Redis

MAX_CACHE_TIMEOUT = 60 * 5


class CacheAbstract(ABC):

    @abstractmethod
    async def _get_from_cache_single(
        self, key: str, model: BaseModel
    ) -> BaseModel | None:
        pass

    @abstractmethod
    async def _get_from_cache_many(
        self, key: str, model: BaseModel
    ) -> list[BaseModel] | None:
        pass

    @abstractmethod
    async def _put_to_cache_single(self, key: str, data: BaseModel) -> None:
        pass

    @abstractmethod
    async def _put_to_cache_many(self, key: str, data: list[BaseModel]) -> None:
        pass


class CacheRedis(CacheAbstract):

    def __init__(self, redis: Redis):
        self.redis = redis

    async def _get_from_cache_single(
        self, key: str, model: BaseModel
    ) -> BaseModel | None:
        data = await self.redis.get(key)
        if not data:
            return None
        return model.parse_raw(data)

    async def _get_from_cache_many(
        self, key: str, model: BaseModel
    ) -> list[BaseModel] | None:
        redis_keys = await self.redis.keys(f"{key}*")
        data = [await self.redis.get(k) for k in redis_keys]
        if not data:
            return None
        return [model.parse_raw(item) for item in data]

    async def _put_to_cache_single(self, key: str, data: BaseModel) -> None:
        await self.redis.set(key, data.json(), MAX_CACHE_TIMEOUT)

    async def _put_to_cache_many(self, key: str, data: list[BaseModel]) -> None:
        for indx, item in enumerate(data):
            await self.redis.set(f"{key}:{indx}", item.json(), MAX_CACHE_TIMEOUT)
