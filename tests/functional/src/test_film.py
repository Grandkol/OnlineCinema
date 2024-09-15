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
    bulk_query
)
from functional.testdata.film_data import SEARCH_FILM_DATA, FILM_DATA
from functional.testdata.es_mapping import MAPPING_MOVIES


API_FILMS_SEARCH = "films/search"
API_FILMS = "films/"

@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "The Star Maker"},
         {"status": 200, "length": 50})
     ],
)
@pytest.mark.asyncio
async def test_film_search(es_write_data, make_get_request, bulk_query, query_data, expected_answer):
    # 1. Генерируем данные для ES
    bulk_query = bulk_query('movies', SEARCH_FILM_DATA)
    # 2. Загружаем данные в ES
    await es_write_data(MAPPING_MOVIES, bulk_query)
    time.sleep(1)
    # 3. Запрашиваем данные из ES по API
    response = await make_get_request(API_FILMS_SEARCH, query_data)
    # 4. Проверяем ответ
    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [({}, {"status": 200, "length": 8})],
)
@pytest.mark.asyncio
async def test_film(es_write_data, make_get_request, bulk_query, query_data, expected_answer):
    # 1. Генерируем данные для ES
    bulk_query = bulk_query('movies', FILM_DATA)
    # 2. Загружаем данные в ES
    await es_write_data(MAPPING_MOVIES, bulk_query)
    # 3. Запрашиваем данные из ES по API
    response = await make_get_request(API_FILMS + '1acfccf3-c5f5-4b98-9456-24e3d553a604', query_data)
    # 4. Проверяем ответ
    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]

