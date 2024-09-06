from pydantic import BaseModel



MAX_CACHE_TIMEOUT = 60 * 5


class BaseCacheService:
    model = None

    async def _get_from_cache(self, key: str):
        data = await self.redis.get(key)
        if not data:
            return None
        person = self.model.parse_raw(data)
        return person
    
    async def _put_to_cache(self, key: str, model: BaseModel | list[BaseModel]):
        if isinstance(model, list):
            for indx, item in enumerate(model):
                await self.redis.set(f'{key}:{indx}', item.json(), MAX_CACHE_TIMEOUT)
        else:
            await self.redis.set(key, model.json(), MAX_CACHE_TIMEOUT)