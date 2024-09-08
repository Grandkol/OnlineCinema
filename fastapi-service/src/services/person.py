from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import FilmList
from models.person import Person
from redis.asyncio import Redis
from services import film
from services.base import BaseService

PERSON_MAX_CACHE_TIMEOUT = 5


class PersonService(BaseService):
    index = "persons"

    async def get_movie_by_person(self, person_id: str) -> FilmList:
        key = f"{self.index}:{person_id}:film"
        result_data = await self._get_from_cache(key, FilmList, many=True)
        if not result_data:
            person_data = await self.get_by_id(person_id)
            result_data = []
            for movie in person_data.films:
                movie_id = movie["id"]
                movie_data = await film.get_film_service(
                    self.redis, self.elastic
                ).get_by_id(movie_id)
                result_data.append(
                    FilmList(
                        id=movie_data.id,
                        title=movie_data.title,
                        imdb_rating=movie_data.imdb_rating,
                    )
                )
            if not result_data:
                return None
            await self._put_to_cache(key, result_data)
        return result_data

    async def search_person(
        self, query: str, page_number: int, page_size: int
    ) -> list[Person] | None:
        key = f"{self.index}:{query}:{page_size}:{page_number}"
        if not query:
            query = ""
        persons = await self._get_from_cache(key, Person, many=True)
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
            persons = await self._search_from_elastic(
                size=page_size, from_=from_, query=statement
            )
            if not persons:
                return None
            await self._put_to_cache(key, persons)
        return persons

    async def _search_from_elastic(
        self, size: int, from_: int, query: dict
    ) -> list[Person]:
        persons = await self.elastic.search(
            index="persons", query=query, from_=int(from_), size=int(size)
        )
        persons = persons["hits"]["hits"]
        return [Person(**person["_source"]) for person in persons]


@lru_cache
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis=redis, elastic=elastic)
