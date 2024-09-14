from abc import ABC, abstractmethod
from pydantic import BaseModel
from elasticsearch import AsyncElasticsearch, NotFoundError


class StorageAbstract(ABC):

    @abstractmethod
    async def _get_item_from_storage(
        self, item_id: str, model: BaseModel, *args, **kwargs
    ) -> BaseModel | None:
        pass

    @abstractmethod
    async def _get_all_from_storage(
        self, page_size: int, page_number: int, model: BaseModel, *args, **kwargs
    ):
        pass


class AbstractStoragePerson(ABC):

    @abstractmethod
    async def _search_from_storage(
        self, size: int, from_: int, query: dict, model: BaseModel, **kwargs
    ) -> list[BaseModel]:
        pass


class StorageBaseElastic(StorageAbstract):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def _get_item_from_storage(
        self, item_id: str, model: BaseModel, *args, **kwargs
    ) -> BaseModel | None:
        index = kwargs.get("index", None)
        if not index:
            raise ValueError(
                "Для работы с Elasticsearch нужно передать index в вызове функции."
            )
        try:
            doc = await self.elastic.get(index=index, id=item_id)
        except NotFoundError:
            return None
        return model(**doc["_source"])

    async def _get_all_from_storage(
        self, page_size: int, page_number: int, model: BaseModel, *args, **kwargs
    ):
        index = kwargs.get("index", None)
        if not index:
            raise ValueError(
                "Для работы с Elasticsearch нужно передать index в вызове функции."
            )
        doc = {"match_all": {}}
        page_number = (page_number - 1) * page_size
        items = await self.elastic.search(
            index=index, query=doc, size=page_size, from_=page_number
        )
        items = items["hits"]["hits"]
        return [model(**item["_source"]) for item in items]


class StoragePersonElastic(StorageBaseElastic, AbstractStoragePerson):

    async def _search_from_storage(
        self, size: int, from_: int, query: dict, model: BaseModel, **kwargs
    ) -> list[BaseModel]:
        index = kwargs.get("index", None) or "persons"
        persons = await self.elastic.search(
            index=index, query=query, from_=int(from_), size=int(size)
        )
        persons = persons["hits"]["hits"]
        return [model(**person["_source"]) for person in persons]


class StorageFilmElastic(StorageBaseElastic):
    pass
