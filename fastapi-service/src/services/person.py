from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film, FilmList
from models.person import Person
from redis.asyncio import Redis
from services.base import AbstractPersonService, BaseElasticService, BaseService
from services.cache import CacheRedis
from services.storage import StoragePersonElastic
from services.film import BaseFilmService

PERSON_MAX_CACHE_TIMEOUT = 5


class BasePersonService(BaseService, AbstractPersonService):

    async def get_movie_by_person(self, person_id: str) -> FilmList:
        key = f"{self.index}:{person_id}:film"
        result_data = await self.cache._get_from_cache_many(key, FilmList)
        if not result_data:
            person_data = await self.storage._get_item_from_storage(
                person_id, Person, index="persons"
            )
            if not person_data:
                return False
            result_data = []
            for movie in person_data.films:
                movie_id = movie["id"]
                movie_data = await self.storage._get_item_from_storage(
                    movie_id, Film, index="movies"
                )
                if not movie_data:
                    return None
                result_data.append(
                    FilmList(
                        id=movie_data.id,
                        title=movie_data.title,
                        imdb_rating=movie_data.imdb_rating,
                    )
                )
            if not result_data:
                return None
            await self.cache._put_to_cache_many(key, result_data)
        return result_data

    async def search_person(
        self, query: str, page_number: int, page_size: int
    ) -> list[Person] | None:
        key = f"{self.index}:{query}:{page_size}:{page_number}"
        if not query:
            query = ""
        persons = await self.cache._get_from_cache_many(key, Person)
        if not persons:
            statement = {
                "match": {
                    "full_name": {
                        "query": query,
                        "fuzziness": "auto",
                    }
                }
            }
            from_ = (page_number - 1) * page_size
            persons = await self.storage._search_from_storage(
                size=page_size, from_=from_, query=statement, model=Person
            )
            if not persons:
                return None
            await self.cache._put_to_cache_many(key, persons)
        return persons


class ElasticServicePerson(
    BaseElasticService,
    BasePersonService,
):
    index = "persons"

    def __init__(self, cache: CacheRedis, storage: StoragePersonElastic):
        super().__init__(cache, storage)
        self.storage = storage


@lru_cache
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticServicePerson:
    return ElasticServicePerson(
        cache=CacheRedis(redis), storage=StoragePersonElastic(elastic)
    )
