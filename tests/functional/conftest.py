import pytest_asyncio
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import asyncio
import aiohttp
import time
import json
from functional.settings import test_settings

pytest_plugins = "functional.fixtures"

def load_schema(index: str) -> str:
    """Функция читает схему из файла

    Args:
        path_file (str): Файл схемы.

    Returns:
        str: Схема, полученная из файла.
    """
    path_file = f"/tests/functional/testdata/schemas/schema-{index}.json"
    with open(path_file, "r") as file:
        schema = json.load(file)
    return schema


@pytest_asyncio.fixture(name="redis", scope="function")
async def redis() -> Redis:
    redis = await Redis(
        host=test_settings.redis_host, port=test_settings.redis_port, decode_responses=True
    )
    await redis.flushall()
    yield redis
    await redis.aclose()


@pytest_asyncio.fixture(name="bulk_query", scope="session")
def bulk_query():
    def inner(index, data):
        es_data = data
        bulk_query: list[dict] = []
        for row in es_data:
            data = {"_index": index, "_id": row["id"], "refresh":"wait_for"}
            data.update({"_source": row})
            bulk_query.append(data)

        return bulk_query

    return inner


@pytest_asyncio.fixture(name="es_write_data", scope="session")
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(mapping, index: str, data: list[dict]):
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)
        await es_client.indices.create(
            index=index, mappings=mapping["mappings"], settings=mapping["settings"]
        )
        updated, errors = await async_bulk(client=es_client, actions=data)
        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest_asyncio.fixture(name="make_get_request", scope="session")
def make_get_request(client_session):
    async def inner(endpoint, query_data: list[dict] | None = None):
        url = test_settings.service_url + endpoint
        print(f'current_fixture={url}')
        async with client_session.get(url, params=query_data) as response:
            body = await response.json()
            status = response.status
        return body, status

    return inner
