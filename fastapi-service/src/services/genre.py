from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.genres import BaseGenre
from redis.asyncio import Redis
from cache import CacheRedis
from storage import StorageGenreElastic
from base import BaseService, BaseElasticService


class BaseGenreService(BaseService):
    async def get_all(self, page_size: int, page_number: int, *args, **kwargs):
        super().get_all(page_size, page_number, model=BaseGenre)


class ElasticServiceGenre(BaseGenreService, BaseElasticService):
    index = "genres"


@lru_cache
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticServiceGenre:
    return ElasticServiceGenre(
        cache=CacheRedis(redis), storage=StorageGenreElastic(elastic)
    )
