import datetime
import uuid
import time
import asyncio
import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from functional.settings import test_settings
from functional.conftest import _load_schema
from functional.testdata.genre_data import GENRE_DATA

API_ALL_GENREs = "genres/"
API_FILMS = "persons/"
SCHEMA = _load_schema("persons")


@pytest.mark.parametrize(
    "query_data, expected_answer, response_template",
    [
        (
            {"page_number": "2", "page_size": "1"},
            {"status": 200, "length": 1},
            {"id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5", "name": "Romance"},
        ),
        ({"page_number": "1", "page_size": "50"}, {"status": 200, "length": 26}, None),
    ],
)
@pytest.mark.asyncio
async def test_genre_search(
    es_write_data,
    make_get_request,
    bulk_query,
    query_data,
    expected_answer,
    response_template,
):

    bulk_query = bulk_query("genres", GENRE_DATA)
    await es_write_data(SCHEMA, "persons", bulk_query)
    asyncio.sleep(1)
    response = await make_get_request("genres", query_data)
    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]
    if response_template:
        assert response[0][0] == response_template


@pytest.mark.parametrize(
    "query_data, expected_answer, response_template",
    [
        (
            {"page_number": "2", "page_size": "1"},
            {"status": 200, "length": 1},
            {"id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5", "name": "Romance"},
        ),
        ({"page_number": "1", "page_size": "50"}, {"status": 200, "length": 26}, None),
    ],
)
@pytest.mark.asyncio
async def test_genre_detail(
    es_write_data,
    make_get_request,
    bulk_query,
    query_data,
    expected_answer,
    response_template,
):

    bulk_query = bulk_query("genres", GENRE_DATA)
    await es_write_data(SCHEMA, "persons", bulk_query)
    asyncio.sleep(1)
    response = await make_get_request("genres", query_data)
    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]
    if response_template:
        assert response[0][0] == response_template
