import pytest_asyncio
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import pytest_asyncio
import asyncio
import aiohttp

import pytest
from functional.settings import test_settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="es_client", scope="session")
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name="client_session", scope="session")
async def client_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name="redis", scope='session')
async def redis() -> Redis:
    redis = await Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    await redis.flushall()
    yield redis
    redis.close()


@pytest_asyncio.fixture(name="bulk_query", scope="session")
def bulk_query():
    def inner(index, data):
        es_data = data

        bulk_query: list[dict] = []
        for row in es_data:
            data = {"_index": index, "_id": row["id"]}
            data.update({"_source": row})
            bulk_query.append(data)

        return bulk_query
    return inner


@pytest_asyncio.fixture(name="es_write_data", scope="session")
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(mapping, data: list[dict]):
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(index=test_settings.es_index, **mapping)
        updated, errors = await async_bulk(client=es_client, actions=data)
        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest_asyncio.fixture(name="make_get_request", scope="session")
def make_get_request(client_session):
    async def inner(endpoint, query_data: list[dict]):
        url = test_settings.service_url + endpoint
        async with client_session.get(url, params=query_data) as response:
            body = await response.json()
            status = response.status
        return body, status

    return inner
