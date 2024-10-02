from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film, FilmList
from redis.asyncio import Redis
from services.base import AbstractFilmService, BaseService
from services.cache import CacheRedis
from services.storage import AbstractStorageFilm, StorageFilmElastic


class BaseFilmService(BaseService, AbstractFilmService):
    def __init__(self, cache: CacheRedis, storage: AbstractStorageFilm):
        super().__init__(cache, storage)
        self.storage = storage

    async def get_film_list(
        self, sort: str, genre: str, page_size: int, page_number: int, query: str
    ) -> list[Film] | None:
        key = f"{self.index}:{query}:{page_size}:{page_number}:{sort}:{genre}"
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


class ElasticServiceFilm(
    BaseFilmService,
):
    index = "movies"


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticServiceFilm:
    return ElasticServiceFilm(CacheRedis(redis), StorageFilmElastic(elastic))
