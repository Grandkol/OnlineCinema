from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis
from pydantic import BaseModel

from models.person import Person
from db.elastic import get_elastic
from db.redis import get_redis


PERSON_MAX_CACHE_TIMEOUT = 60 * 5

class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str):
        person = self._get_from_cache(person_id)
        if not person:
            person = self._get_from_elastic(person_id)
            if not person:
                return None
            self._put_to_cache(person)
        return person
    
    async def _get_from_elastic(self, person_id: str):
        try:
            person = await self.elastic.get(index='persons', id=person_id)
        except NotFoundError:
            return None
        return Person(**person['_source'])
    
    async def _get_from_cache(self, person_id: str):
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person
    
    async def _put_to_cache(self, person: Person):
        await self.redis.set(person.id, person.json(), PERSON_MAX_CACHE_TIMEOUT)


    async def get_all(self):
        persons = self._get_all_from_elastic()
        for person in self._get_all_from_elastic():
            yield Person(**person['_source'])


    async def _get_all_from_elastic(self):
        doc = {
            'size' : 10000,
            'query': {
                'match_all' : {}
                }
            }
        persons = self.elastic.search(index='person', query=doc)
        for person in persons:
            yield person



@lru_cache
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(redis=redis, elastic=elastic)
    


