from abc import ABC, abstractmethod

from elasticsearch import AsyncElasticsearch, NotFoundError
from models.film import FilmList
from pydantic import BaseModel


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


class AbstractStorageFilm(ABC):

    @abstractmethod
    async def _get_list_from_storage(
        self, sort: str, genre: str, page_size: int, page_number: int, query: str
    ) -> list[BaseModel] | None:
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
            print(item_id, index, model)
            doc = await self.elastic.get(index=index, id=item_id)
            print(doc)
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


class StorageFilmElastic(StorageBaseElastic, AbstractStorageFilm):

    async def _get_list_from_storage(
        self,
        sort: str,
        genre: str,
        page_size: int,
        page_number: int,
        query: str,
        model: BaseModel = FilmList,
    ) -> list[BaseModel] | None:
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
                            "bool": {
                              "must": [
                                {
                                  "match": {
                                    "genres.id": genre
                                  }
                                }
                              ]
                            }
                          }
                        }
                    }
                }

            doc = await self.elastic.search(index="movies", body=body_query)
            documents = doc["hits"]["hits"]
        except NotFoundError:
            return None
        return [model(**document["_source"]) for document in documents]
