from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis
from services.base import BaseService
from services.cache import CacheRedis
from services.storage import StorageBaseElastic


class ElasticServiceGenre(BaseService):
    index = "genres"


@lru_cache
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticServiceGenre:
    return ElasticServiceGenre(
        cache=CacheRedis(redis), storage=StorageBaseElastic(elastic)
    )
