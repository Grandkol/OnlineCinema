from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import pytest_asyncio
import asyncio
import aiohttp

import pytest
from functional.settings import test_settings
from functional.testdata.es_mapping import MAPPING_MOVIES


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='client_session', scope='session')
async def client_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict]):
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(index=test_settings.es_index, **MAPPING_MOVIES)
        print(data)

        updated, errors = await async_bulk(client=es_client, actions=data)

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(client_session):
    async def inner(endpoint, query_data: list[dict]):
        url = test_settings.service_url + endpoint
        print(url)
        async with client_session.get(url, params=query_data) as response:
            body = await response.json()
            print(body)
            status = response.status
        return body, status

    return inner
