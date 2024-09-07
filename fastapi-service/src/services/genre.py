from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.genres import BaseGenre, Genre
from redis.asyncio import Redis
from services.cache import BaseCacheService


class GenreService(BaseCacheService):
    index = "genres"

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str):
        key = f"{self.index}:{genre_id}"
        genre = await self._get_from_cache(key, Genre)
        if not genre:
            genre = await self._get_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_to_cache(key, genre)
        return genre

    async def _get_from_elastic(self, item_id: str):
        try:
            genre = await self.elastic.get(index="genres", id=item_id)
        except NotFoundError:
            return None
        data = genre["_source"]
        return Genre(**data)

    async def _get_all_from_elastic(self, page_size: int, page_number: int):
        doc = {"match_all": {}}
        page_number = (page_number - 1) * page_size
        genres = await self.elastic.search(
            index="genres", query=doc, size=page_size, from_=page_number
        )
        genres = genres["hits"]["hits"]
        return [
            BaseGenre(
                id=genre["_source"]["id"],
                name=genre["_source"]["name"],
                description=genre["_source"]["description"],
            )
            for genre in genres
        ]

    async def get_all(self, page_size: int, page_number: int):
        key = f"{self.index}:{page_size}:{page_number}"
        genres = await self._get_from_cache(key, BaseGenre, many=True)
        if not genres:
            genres = await self._get_all_from_elastic(
                page_size=page_size, page_number=page_number
            )
            if not genres:
                return None
            await self._put_to_cache(key, genres)
        return genres


@lru_cache
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis=redis, elastic=elastic)
