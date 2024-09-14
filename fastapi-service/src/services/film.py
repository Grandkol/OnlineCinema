from functools import lru_cache

from base import AbstractFilmService, BaseElasticService, BaseService
from cache import CacheRedis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis
from storage import StorageFilmElastic

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmList
from services.base import BaseService


class BaseFilmService(BaseService, AbstractFilmService):

    async def get_film_list(
        self, sort: str, genre: str, page_size: int, page_number: int, query: str
    ) -> list[Film] | None:
        key = f"{self.index}:{query}:{page_size}:{page_number}"
        films = await self.cache._get_from_cache_many(key, FilmList)
        if not films:
            films = await self.storage._get_list_from_storage(
                sort=sort,
                genre=genre,
                page_size=page_size,
                page_number=page_number,
                query=query,
            )
            if not films:
                return None
            await self.cache._put_to_cache_many(key, films)
        return films


class ElasticServiceFilm(BaseFilmService, BaseElasticService):
    index = "movies"

    def __init__(self, cache: CacheRedis, storage: StorageFilmElastic):
        super().__init__(cache, storage)
        self.storage = storage


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticServiceFilm:
    return ElasticServiceFilm(redis, elastic)
