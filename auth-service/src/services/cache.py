from redis.asyncio import Redis

class RedisCache:
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, decode_responses=True)
    async def _put_to_redis(self, key: str, token: str) -> None:
        return await self.redis.set(key, token)

    async def _get_from_redis(self: Redis, key: str) -> None:
        return await self.redis.get(key)

    async def _delete_from_redis(self: Redis, key: str) -> None:
        return await self.redis.delete(key)

    async def _get_redis_keys(self: Redis):
        return await self.redis.keys()


redis = RedisCache()
