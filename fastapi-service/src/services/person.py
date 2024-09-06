from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis
from pydantic import BaseModel

from services import film
from models.film import FilmList
from models.person import Person
from db.elastic import get_elastic
from db.redis import get_redis
import logging

logger = logging.getLogger('person')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


PERSON_MAX_CACHE_TIMEOUT = 60 * 5

class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str):
        key = f'persons:{person_id}'
        person = await self._get_from_cache(key)
        if not person:
            person = await self._get_from_elastic(key)
            if not person:
                return None
            # await self._put_to_cache(person)
        return person
    
    async def get_movie_by_person(self, person_id: str):
        person_data = await self.get_by_id(person_id)
        result_data = []
        for movie in person_data.films:
            movie_id = movie['id']
            movie_data = await film.get_film_service(self.redis, self.elastic).get_by_id(movie_id)
            result_data.append(FilmList(id=movie_data.id,
                                    title=movie_data.title,
                                    imdb_rating=movie_data.imdb_rating                                   
                                    ))
        return result_data

    async def search_person(self, query: str, page_number: int, page_size: int):
        statement = {
        "match": {
            "full_name": {
                "query": query, 
                "fuzziness": "auto",
            }
        }
    }
        from_ = (page_number - 1) * page_size
        persons = await self._search_from_elastic(size=page_size, from_=from_, query=statement )
        persons = persons['hits']['hits']
        return [Person(**person['_source']) for person in persons]

    async def _search_from_elastic(self, size: int, from_: int, query: dict):
        persons = await self.elastic.search(index='persons', query=query, from_=int(from_), size=int(size))
        return persons


    async def _get_from_elastic(self, person_id: str):
        try:
            person = await self.elastic.get(index='persons', id=person_id)
        except NotFoundError:
            return None
        data = person['_source']
        return Person(**data)
    

    async def get_all(self, page_size: int, page_number: int):
        return [Person(**person['_source']) for person in await self._get_all_from_elastic(page_size, page_number)]


    async def _get_all_from_elastic(self, page_size: int, page_number: int):
        doc = {
                'match_all' : {}
                }
        page_number = (page_number - 1) * page_size
        persons = await self.elastic.search(index='persons', query=doc, from_=page_number, size=page_size)
        persons = persons['hits']['hits']
        return persons



    async def _get_from_cache(self, person_id: str):
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person
    
    async def _put_to_cache(self, key: str, person: Person | list):
            await self.redis.set(key, person.json(), PERSON_MAX_CACHE_TIMEOUT)

@lru_cache
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(redis=redis, elastic=elastic)
    


