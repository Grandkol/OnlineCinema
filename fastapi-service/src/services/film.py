from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film, FilmList
from redis.asyncio import Redis
from services.base import BaseService


class FilmService(BaseService):
    index = "movies"

    async def get_film_list(
        self, sort, genre, page_size, page_number, query
    ) -> list[Film] | None:
        key = f"{self.index}:{query}:{page_size}:{page_number}"
        films = await self._get_from_cache(key, FilmList, many=True)
        if not films:
            films = await self._get_list_from_elastic(
                sort=sort,
                genre=genre,
                page_size=page_size,
                page_number=page_number,
                query=query,
            )
            if not films:
                return None
            await self._put_to_cache(key, films)
        return films

    async def _get_list_from_elastic(
        self, sort, genre, page_size, page_number, query
    ) -> list[Film] | None:
        try:
            body_query = {}
            if page_size:
                body_query["size"] = page_size
            if page_number:
                body_query["from"] = (page_number - 1) * page_size

            if sort == "-imdb_rating":
                body_query["sort"] = {"imdb_rating": "desc"}
            if query:
                body_query["query"] = {
                    "multi_match": {
                        "query": query,
                        "fields": ["*"],
                        "fuzziness": "AUTO",
                    }
                }
            if genre:
                body_query["sort"] = {
                    "genres.id": {
                        "mode": "max",
                        "order": "asc",
                        "nested": {
                            "path": "genres",
                            "filter": {
                                "bool": {"must": [{"match": {"genres.id": genre}}]}
                            },
                        },
                    }
                }

            doc = await self.elastic.search(index="movies", body=body_query)

            documents = doc["hits"]["hits"]
        except NotFoundError:
            return None

        return [FilmList(**document["_source"]) for document in documents]

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
