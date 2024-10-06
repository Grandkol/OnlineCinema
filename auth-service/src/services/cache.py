# from abc import ABC, abstractmethod
#
# from pydantic import BaseModel
# from redis.asyncio import Redis
#
# class RedisCache:
#     def __init__(self):
#         self.redis = Redis(host='localhost', port=6379, decode_responses=True)
#     async def _put_to_redis(self, key: str, token: str) -> None:
#         return await self.redis.set(key=key, token=token)
#
#     async def _get_from_redis(self: Redis, key: str) -> None:
#         print(await self.redis.keys())
#         return await self.redis.get(key)
#
# redis = RedisCache()