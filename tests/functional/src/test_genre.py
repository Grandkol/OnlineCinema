import time
import asyncio
import pytest
from http import HTTPStatus
from functional.conftest import load_schema
from functional.testdata.genre_data import GENRE_DATA

API_GENRES = "genres/"
SCHEMA = load_schema("genres")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"page_number": "2", "page_size": "1"},
            {"status": HTTPStatus.OK, "length": 1},
        ),
        (
            {"page_number": "1", "page_size": "50"},
            {"status": HTTPStatus.OK, "length": 10},
        ),
    ],
)
@pytest.mark.asyncio
async def test_genre_search(
    es_write_data,
    make_get_request,
    bulk_query,
    query_data,
    expected_answer,
):

    bulk_query = bulk_query("genres", GENRE_DATA)
    await es_write_data(SCHEMA, "genres", bulk_query)

    response = await make_get_request(API_GENRES, query_data)

    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]


@pytest.mark.parametrize(
    "genre_id, status",
    [
        (
            GENRE_DATA[0]["id"],
            HTTPStatus.OK,
        ),
        ("121212121212121212", HTTPStatus.NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_genre_detail(
    es_write_data,
    make_get_request,
    bulk_query,
    genre_id,
    status,
):
    bulk_query = bulk_query("genres", GENRE_DATA)
    await es_write_data(SCHEMA, "genres", bulk_query)

    response = await make_get_request(API_GENRES + genre_id)

    assert response[1] == status


@pytest.mark.parametrize(
    "query_data, length",
    [
        ({"page_num": 1, "page_size": 7}, 7),
    ],
)
@pytest.mark.asyncio
async def test_genre_cache_search(
    es_write_data, make_get_request, bulk_query, redis, query_data, length
):

    bulk_query = bulk_query("genres", GENRE_DATA)
    await es_write_data(SCHEMA, "genres", bulk_query)

    response_1 = await make_get_request(API_GENRES, query_data)
    redis_keys = await redis.keys("*")
    assert len(redis_keys) == length

    response_2 = await make_get_request(API_GENRES, query_data)
    assert response_1[0] == response_2[0]


@pytest.mark.parametrize(
    "genre_id, key, length",
    [
        (GENRE_DATA[0]["id"], f'genres:{GENRE_DATA[0]["id"]}:detail', 1),
    ],
)
@pytest.mark.asyncio
async def test_genre_cache_detail(
    es_write_data,
    make_get_request,
    bulk_query,
    genre_id,
    redis,
    key,
    length,
):
    bulk_query = bulk_query("genres", GENRE_DATA)
    await es_write_data(SCHEMA, "genres", bulk_query)

    response_1 = await make_get_request(API_GENRES + genre_id)
    redis_keys = await redis.keys("*")

    assert len(redis_keys) == length
    assert key == redis_keys[0]

    response_2 = await make_get_request(API_GENRES + genre_id)

    assert response_1[0] == response_2[0]
