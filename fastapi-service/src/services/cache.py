from pydantic import BaseModel



PERSON_MAX_CACHE_TIMEOUT = 60 * 5
GENRE_MAX_CACHE_TIMEOUT = 60 * 5

class BaseCacheService:
    model = None

    async def _get_from_cache(self, key: str):
        data = await self.redis.get(key)
        if not data:
            return None
        person = self.model.parse_raw(data)
        return person
    
    async def _put_to_cache(self, key: str, model: BaseModel):
            await self.redis.set(key, model.json(), PERSON_MAX_CACHE_TIMEOUT)