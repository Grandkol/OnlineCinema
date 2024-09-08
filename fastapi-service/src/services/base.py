from elasticsearch import AsyncElasticsearch, NotFoundError
from models.film import Film
from models.genres import Genre
from models.person import Person
from pydantic import BaseModel
from redis.asyncio import Redis

MAX_CACHE_TIMEOUT = 60 * 5


class BaseService:
    models = {"movies": Film, "persons": Person, "genres": Genre}
    index: str | None = None

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, item_id: str) -> BaseModel | None:
        key = f"{self.index}:{item_id}"
        item = await self._get_from_cache(key, self.models[self.index])
        if not item:
            item = await self._get_item_from_elastic(item_id)
            if not item:
                return None
            await self._put_to_cache(key, item)
        return item

    async def _get_item_from_elastic(self, item_id: str) -> BaseModel | None:
        try:
            doc = await self.elastic.get(index=self.index, id=item_id)
        except NotFoundError:
            return None
        return self.models[self.index](**doc["_source"])

    async def _get_all_from_elastic(self, page_size: int, page_number: int):
        doc = {"match_all": {}}
        page_number = (page_number - 1) * page_size
        items = await self.elastic.search(
            index=self.index, query=doc, size=page_size, from_=page_number
        )
        items = items["hits"]["hits"]
        return [self.models[self.index](**item["_source"]) for item in items]

    async def get_all(self, page_size: int, page_number: int):
        key = f"{self.index}:{page_size}:{page_number}:all"
        items = await self._get_from_cache(key, self.models[self.index], many=True)
        if not items:
            items = await self._get_all_from_elastic(page_size, page_number)
            if not items:
                return None
            await self._put_to_cache(key, items)
        return items

    async def _get_from_cache(
        self, key: str, model: BaseModel, many: bool = False
    ) -> BaseModel | None:

        if many:
            redis_keys = await self.redis.keys(f"{key}*")
            data = [await self.redis.get(k) for k in redis_keys]
            if not data:
                return None
            return [model.parse_raw(item) for item in data]
        data = await self.redis.get(key)
        if not data:
            return None
        return model.parse_raw(data)

    async def _put_to_cache(self, key: str, data: BaseModel | list[BaseModel]) -> None:
        if isinstance(data, list):
            for indx, item in enumerate(data):
                await self.redis.set(f"{key}:{indx}", item.json(), MAX_CACHE_TIMEOUT)
        else:
            await self.redis.set(key, data.json(), MAX_CACHE_TIMEOUT)
