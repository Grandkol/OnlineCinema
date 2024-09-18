import datetime
import uuid
import time
import asyncio
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
    "query_data, expected_answer, response",
    [
        (
                {"page_number": "2", "page_size": "1"},
                {"status": 200, "length": 1},
                  {
                    "id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
                    "name": "Romance"
                    }
        ),
                {"page_number": "1", "page_size": "50"},
                {"status": 200, "length": 1},
                None
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
        # (
        #     {"query": "John", "page_number": 0, "page_size": 0},
        #     {"status": 422, "length": 1},
        # ),
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
    
    bulk_query = bulk_query("persons", PERSON_DATA)
    await es_write_data(SCHEMA, "persons", bulk_query)
    asyncio.sleep(1)
    response = await make_get_request(API_PERSON_SEARCH, query_data)
    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]
