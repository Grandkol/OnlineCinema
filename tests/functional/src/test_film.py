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
    redis,
    _load_schema
)
from functional.testdata.film_data import SEARCH_FILM_DATA, FILM_DATA
# from functional.testdata.schemas import MAPPING_MOVIES



API_FILMS_SEARCH = "films/search"
API_FILMS = "films/"
SCHEMA = _load_schema('movies')


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {"query": "The Star Maker",
                 "genre": "1cacff68-643e-4ddd-8f57-84b62538081a",
                 "sort": "-imdb_rating"},
                {"status": 200, "length": 50}
        ),
        (
                {"query": "lalallalal",
                 "genre": "1cacff68-643e-4ddd-8f57-84b62538081a",
                 "sort": "-imdb_rating",
                 "page_number": 1,
                 "page_size": 50},
                {"status": 404, "length": 1}
        ),
        (
                {"query": "The Star Maker",
                 "genre": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
                 "page_number": 1,
                 "page_size": 50},
                {"status": 200, "length": 50}
        ),
        (
                {"query": "The Star Maker",
                 "genre": "1cacff68-643e-4ddd-8f57-84b62538081a",
                 "sort": "-imdb_rating",
                 "page_number": 1,
                 "page_size": 50},
                {"status": 200, "length": 50}
        ),
        (
                {"query": "The Star Maker",
                 "genre": "1cacff68-643e-4ddd-8f57-84b62538081a",
                 "sort": "-imdb_rating",
                 "page_number": "rerrere",
                 "page_size": 50},
                {"status": 422, "length": 1}
        ),
        (
                {"query": "The Star Maker",
                 "genre": "1cacff68-643e-4ddd-8f57-84b62538081a",
                 "sort": "-imdb_rating",
                 "page_number": 1,
                 "page_size": 'rereee'},
                {"status": 422, "length": 1}
        ),
     ],
)
@pytest.mark.asyncio
async def test_film_search(es_write_data, make_get_request, bulk_query, query_data, expected_answer):
    bulk_query = bulk_query('movies', SEARCH_FILM_DATA)

    await es_write_data(SCHEMA, bulk_query)
    time.sleep(1)
    response = await make_get_request(API_FILMS_SEARCH, query_data)

    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]


@pytest.mark.parametrize(
    "film_id, query_data, expected_answer",
    [
        (
                '1acfccf3-c5f5-4b98-9456-24e3d553a604',
                {},
                {"status": 200, "length": 8}
        ),
        (
                'lalalallalalalal',
                {},
                {"status": 404, "length": 1}
        )
    ],
)
@pytest.mark.asyncio
async def test_film(es_write_data, make_get_request, bulk_query, film_id, query_data, expected_answer):
    bulk_query = bulk_query('movies', FILM_DATA)

    await es_write_data(SCHEMA, bulk_query)
    response = await make_get_request(API_FILMS + film_id, query_data)

    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]


@pytest.mark.parametrize(
    "film_id, query_data, expected_answer",
    [
        (
                '1acfccf3-c5f5-4b98-9456-24e3d553a604',
                {},
                {"status": 200, "length": 8}
        )
    ],
)
@pytest.mark.asyncio
async def test_film_cache(es_write_data, make_get_request, bulk_query, film_id, query_data, expected_answer, es_client):
    bulk_query = bulk_query('movies', FILM_DATA)
    await es_write_data(SCHEMA, bulk_query)

    response = await make_get_request(API_FILMS + film_id, query_data)

    assert response[1] == expected_answer["status"]

    await es_client.indices.delete(index="movies")

    response = await make_get_request(API_FILMS + film_id, query_data)

    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {"query": "The Star Maker",
                 "genre": "1cacff68-643e-4ddd-8f57-84b62538081a",
                 "sort": "-imdb_rating",
                 "page_number": 1,
                 "page_size": 50},
                {"status": 200, "length": 50}
        )
    ],
)
@pytest.mark.asyncio
async def test_film_search_cache(es_write_data, make_get_request, bulk_query, query_data, expected_answer, es_client):
    bulk_query = bulk_query('movies', SEARCH_FILM_DATA)
    await es_write_data(SCHEMA, bulk_query)

    response = await make_get_request(API_FILMS_SEARCH, query_data)

    assert response[1] == expected_answer["status"]

    await es_client.indices.delete(index="movies")

    response = await make_get_request(API_FILMS_SEARCH, query_data)

    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]
