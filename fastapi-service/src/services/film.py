from functools import lru_cache
from typing import Optional, List

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis
from pydantic import BaseModel

from models.film import Film, FilmList
from db.elastic import get_elastic
from db.redis import get_redis


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def get_film_list(self, sort, genre, page_size, page_number, query) -> Optional[List[Film]]:
        #Тут вытаскиваем из redis

        list = await self._get_list_from_elastic(sort=sort,
                                                 genre=genre,
                                                 page_size=page_size,
                                                 page_number=page_number,
                                                 query=query)
        if not list:
            return None

        #Тут кладем в редис
        return list


    async def _get_list_from_elastic(self, sort, genre, page_size, page_number, query) -> Optional[List[Film]]:
        try:
            body_query = {}
            if page_size:
                body_query["size"] = page_size
            if page_number:
                body_query["from"] = (page_number-1)*page_size

            if sort == "-imdb_rating":
                body_query["sort"] = {
                    "imdb_rating": "desc"
                }
            if query:
                body_query["query"] = {
                    "multi_match": {
                        "query": query,
                        "fields": ["*"],
                        "fuzziness": "AUTO",
                    }
                }

            doc = await self.elastic.search(
                index="movies",
                body=body_query
            )

            documents = doc["hits"]["hits"]
        except NotFoundError:
            return None

        return [FilmList(**document['_source']) for document in documents]

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
