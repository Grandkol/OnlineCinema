import datetime
import uuid
import time

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from functional.settings import test_settings
from functional.conftest import es_write_data, es_client, event_loop


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
async def test_search(es_write_data, query_data, expected_answer):
    # 1. Генерируем данные для ES
    es_data = [{
        'id': str(uuid.uuid4()),
        "title": "The Star Maker",
        "imdb_rating": 7.4,
        "description": "\"Dottore\" Joe Moretti travels round Sicily doing screen tests for the big Roman studios. "
                       "He's a conman and takes money or favours for his efforts. Beata, a young illiterate convent "
                       "girl desperately wants to change her life and falls for him, belatedly he realises his feelings "
                       "for her. Their love affair is doomed when he's arrested.",
        "genres": [
            {
                "id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
                "name": "Romance"
            },
            {
                "id": "1cacff68-643e-4ddd-8f57-84b62538081a",
                "name": "Drama"
            }
        ],
        "actors": [
            {
                "id": "a88f14e6-a8e2-4e05-9744-e89fadf960fb",
                "name": "Franco Scaldati"
            },
            {
                "id": "6d5964ff-e56e-40aa-9e30-6a52ed741e55",
                "name": "Leopoldo Trieste"
            },
            {
                "id": "e1d02f5f-bd47-4eb4-a9c3-1f353ffa9e54",
                "name": "Sergio Castellitto"
            },
            {
                "id": "f142081a-8054-4ec3-ae97-026f8ebdef3e",
                "name": "Tiziana Lodato"
            }
        ],
        "writers": [
            {
                "id": "55dc3cfa-0731-42fe-9d7b-6180b00ab712",
                "name": "Giuseppe Tornatore"
            },
            {
                "id": "c740cb33-df3a-4aeb-b3ad-7e79581d857c",
                "name": "Fabio Rinaudo"
            }
        ],
        "directors": [
            {
                "id": "55dc3cfa-0731-42fe-9d7b-6180b00ab712",
                "name": "Giuseppe Tornatore"
            }
        ]
    } for _ in range(60)]

    bulk_query: list[dict] = []
    for row in es_data:
        data = {'_index': 'movies', '_id': row['id']}
        data.update({'_source': row})
        bulk_query.append(data)

    # 2. Загружаем данные в ES
    await es_write_data(bulk_query)
    time.sleep(5)
    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/films/search'
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        print(body)
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']