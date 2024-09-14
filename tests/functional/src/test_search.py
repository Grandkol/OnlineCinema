import datetime
import uuid
import time

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from functional.settings import test_settings
from functional.conftest import es_write_data, es_client, event_loop, make_get_request, client_session
from functional.testdata.search_data import SEARCH_DATA


API_FILMS = 'films/search'

@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star Maker'},
                {'status': 200, 'length': 50}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data, make_get_request, query_data, expected_answer):
    # 1. Генерируем данные для ES
    es_data = SEARCH_DATA
    bulk_query: list[dict] = []
    for row in es_data:
        data = {'_index': 'movies', '_id': row['id']}
        data.update({'_source': row})
        bulk_query.append(data)

    # 2. Загружаем данные в ES
    await es_write_data(bulk_query)
    time.sleep(3)
    # 3. Запрашиваем данные из ES по API
    response = await make_get_request(API_FILMS, query_data)
    print(response)
    # 4. Проверяем ответ
    assert response[1] == expected_answer['status']
    assert len(response[0]) == expected_answer['length']