from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis
from pydantic import BaseModel

from services import film
from models.genres import Genre, BaseGenre
from db.elastic import get_elastic
from db.redis import get_redis
import logging

logger = logging.getLogger('person')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)



class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str):
        genre = await self._get_from_cache(genre_id)
        if not genre:
            genre = await self._get_from_elastic(genre_id)
            if not genre:
                return None
            # await self._put_to_cache(person)
        return genre
    

    async def _get_from_elastic(self, item_id: str):
        try:
            genre = await self.elastic.get(index='genres', id=item_id)
        except NotFoundError:
            return None
        data = genre['_source']
        return BaseGenre(**data)
    
    async def _get_all_from_elastic(self, page_size: int, page_number: int):
        doc = {
                'match_all' : {}
                }
        page_number = (page_number - 1) * page_size
        genres = await self.elastic.search(index='genres', query=doc, size=page_size, from_=page_number)
        genres = genres['hits']['hits']
        return genres
    
    async def get_all(self, page_size: int, page_number: int):
        genres = await self._get_all_from_elastic(page_size=page_size, page_number=page_number)
        return [Genre(id=genre['_source']['id'], name=genre['_source']['name'], description=genre['_source']['description']) for genre in genres]
    
    async def _get_from_cache(self, person_id: str):
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = Genre.parse_raw(data)
        return person

@lru_cache
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(redis=redis, elastic=elastic)
    


