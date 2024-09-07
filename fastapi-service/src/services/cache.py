from pydantic import BaseModel


MAX_CACHE_TIMEOUT = 60 * 5


class BaseCacheService:

    async def _get_from_cache(self, key: str, model: BaseModel, many: bool = False):

        if many:
            redis_keys = await self.redis.keys(f"{key}*")
            data = [await self.redis.get(k) for k in redis_keys]
            if not data:
                return None
            return [model.parse_raw(item) for item in data]
        data = await self.redis.get(key)
        if not data:
            return None
        return model.parse_raw(data)

    async def _put_to_cache(self, key: str, data: BaseModel | list[BaseModel]):
        if isinstance(data, list):
            for indx, item in enumerate(data):
                await self.redis.set(f"{key}:{indx}", item.json(), MAX_CACHE_TIMEOUT)
        else:
            await self.redis.set(key, data.json(), MAX_CACHE_TIMEOUT)
