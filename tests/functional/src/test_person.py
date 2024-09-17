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
    _load_schema
)
from functional.testdata.person_data import SEARCH_PERSON_DATA

API_PERSON_SEARCH = "persons/search"
API_FILMS = "persons/"
SCHEMA = _load_schema('persons')


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "Nick"},
         {"status": 200, "length": 1})
     ],
)
@pytest.mark.asyncio
async def test_person_search(es_write_data, make_get_request, bulk_query, query_data, expected_answer):
    # 1. Генерируем данные для ES
    bulk_query = bulk_query('persons', SEARCH_PERSON_DATA)
    # 2. Загружаем данные в ES
    await es_write_data(SCHEMA, bulk_query)
    time.sleep(1)
    # 3. Запрашиваем данные из ES по API
    response = await make_get_request(API_PERSON_SEARCH, query_data)
    # 4. Проверяем ответ
    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]