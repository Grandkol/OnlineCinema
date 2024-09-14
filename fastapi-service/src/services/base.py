from abc import ABC, abstractmethod

from cache import CacheAbstract
from pydantic import BaseModel
from storage import StorageAbstract

from models.film import Film
from models.genres import Genre
from models.person import Person


class AbstractService(ABC):

    def __init__(self, cache: CacheAbstract, storage: StorageAbstract):
        self.storage = storage
        self.cache = cache

    @abstractmethod
    async def get_by_id(self, item_id: str):
        pass

    @abstractmethod
    async def get_all(self, page_size: int, page_number: int):
        pass


class AbstractPersonService(ABC):

    @abstractmethod
    async def get_movie_by_person(self, person_id: str) -> BaseModel:
        pass

    @abstractmethod
    async def search_person(
        self, query: str, page_number: int, page_size: int
    ) -> list[BaseModel] | None:
        pass


class AbstractFilmService(ABC):

    @abstractmethod
    async def get_film_list(
        self, sort, genre, page_size, page_number, query
    ) -> list[Film] | None:
        pass


class BaseService(AbstractService):
    models = {"movies": Film, "persons": Person, "genres": Genre}
    index: str | None = None

    async def get_by_id(self, item_id: str, *args, **kwargs) -> BaseModel | None:
        key = f"{self.index}:{item_id}"
        model = kwargs.get("model", None) or self.models[self.index]
        item = await self.cache._get_from_cache_single(key, model)
        if not item:
            item = await self.storage._get_item_from_storage(
                item_id, model, *args, **kwargs
            )
            if not item:
                return None
            await self.cache._put_to_cache_single(key, item)
        return item

    async def get_all(self, page_size: int, page_number: int, *args, **kwargs):
        key = f"{self.index}:{page_size}:{page_number}:all"
        model = kwargs.get("model", None) or self.models[self.index]
        items = await self.cache._get_from_cache_many(key, model)
        if not items:
            items = await self.storage._get_all_from_storage(
                page_size, page_number, model, *args, **kwargs
            )
            if not items:
                return None
            await self.cache._put_to_cache_many(key, items)
        return items


class BaseElasticService(BaseService):

    async def get_by_id(self, item_id: str, *args, **kwargs) -> BaseModel | None:
        index = kwargs.get("index", None) or self.index
        super().get_by_id(item_id, index=index, **kwargs)

    async def get_all(self, page_size: int, page_number: int, *args, **kwargs):
        index = kwargs.get("index", None) or self.index
        super().get_all(page_size, page_number, index=index, **kwargs)
