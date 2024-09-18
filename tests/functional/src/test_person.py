import datetime
import uuid
import time

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from functional.settings import test_settings
from functional.conftest import (
    es_write_data,
    es_client,
    event_loop,
    make_get_request,
    client_session,
    bulk_query,
    _load_schema,
)
from functional.testdata.person_data import SEARCH_PERSON_DATA, PERSON_DATA

API_PERSON_SEARCH = "persons/search"
API_FILMS = "persons/"
SCHEMA = _load_schema("persons")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        # (
        #         {"query": "aaaaa"},
        #         {"status": 404, "length": 1}
        # ),
        # (
        #         {"query": "Nick"},
        #         {"status": 200, "length": 22}
        # ),
        # (
        #         {"query": "Nick", 'page_number': 100, 'page_size': 2},
        #         {"status": 404, "length": 1}
        # ),
        # (
        #         {"query": "John", 'page_number': 1, 'page_size': 4},
        #         {"status": 200, "length": 4}
        # ),
        (
            {"query": "John", "page_number": 0, "page_size": 0},
            {"status": 422, "length": 1},
        ),
        # (
        #         {"query": "Nick", 'page_number': 'ererer', 'page_size': 2},
        #         {"status": 422, "length": 1}
        # ),
        # (
        #         {"query": "Nick", 'page_number': 1, 'page_size': 'qw'},
        #         {"status": 422, "length": 1}
        # ),
    ],
)
@pytest.mark.asyncio
async def test_person_search(
    es_write_data, make_get_request, bulk_query, query_data, expected_answer
):
    # 1. Генерируем данные для ES
    bulk_query = bulk_query("persons", PERSON_DATA)
    # 2. Загружаем данные в ES
    await es_write_data(SCHEMA, "persons", bulk_query)
    time.sleep(1)
    # 3. Запрашиваем данные из ES по API
    response = await make_get_request(API_PERSON_SEARCH, query_data)
    print(response)
    # 4. Проверяем ответ
    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]


@pytest.mark.parametrize(
    "query_data, key, length",
    [
        ({"query": "Star"}, ["persons:Star:50:1:0"], 1),
        # (
        #         {"query": "AAAAA"}, [], 0
        # ),
    ],
)
@pytest.mark.asyncio
async def test_person_detail_cache(
    es_write_data,
    es_client,
    make_get_request,
    bulk_query,
    query_data,
    key,
    length,
    redis,
):
    bulk_query = bulk_query("persons", PERSON_DATA)
    # 2. Загружаем данные в ES
    await es_write_data(SCHEMA, "persons", bulk_query)
    time.sleep(1)
    response_1 = await make_get_request(API_PERSON_SEARCH, query_data)
    redis_keys = await redis.keys("*")
    print(redis_keys)
    assert len(redis_keys) == length
    assert key == redis_keys

    await es_client.indices.delete(index="persons")
    response_2 = await make_get_request(API_PERSON_SEARCH, query_data)

    assert response_1[0] == response_2[0]
