import pytest_asyncio
import asyncio
from elasticsearch import AsyncElasticsearch
import aiohttp

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="es_client", scope="session")
async def es_client():
    es_client = AsyncElasticsearch(hosts=f'http://{test_settings.es_host}:{test_settings.es_port}', verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name="client_session", scope="session")
async def client_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()