from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.genres import BaseGenre
from redis.asyncio import Redis
from services.base import BaseService


class GenreService(BaseService):
    index = "genres"

    async def _get_all_from_elastic(self, page_size: int, page_number: int):
        genres = await super()._get_all_from_elastic(
            page_number=page_number, page_size=page_size
        )
        return [
            BaseGenre(
                id=genre.id,
                name=genre.name,
                description=genre.description,
            )
            for genre in genres
        ]


@lru_cache
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis=redis, elastic=elastic)
