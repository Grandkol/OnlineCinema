import asyncio
import pytest
from tests.conftest import (
    load_schema,
)
from tests.functional.testdata.person_data import PERSON_DATA
from tests.functional.testdata.film_data import FILM_DATA

API_PERSON_SEARCH = "persons/search"
API_PERSON_DETAIL = "persons/"
SCHEMA = load_schema("persons")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "aaaaa"}, {"status": 404, "length": 1}),
        ({"query": "Nick"}, {"status": 200, "length": 22}),
        (
            {"query": "Nick", "page_number": 100, "page_size": 2},
            {"status": 404, "length": 1},
        ),
        (
            {"query": "John", "page_number": 1, "page_size": 4},
            {"status": 200, "length": 4},
        ),
        (
            {"query": "John", "page_number": 0, "page_size": 0},
            {"status": 422, "length": 1},
        ),
        (
            {"query": "Nick", "page_number": "ererer", "page_size": 2},
            {"status": 422, "length": 1},
        ),
        (
            {"query": "Nick", "page_number": 1, "page_size": "qw"},
            {"status": 422, "length": 1},
        ),
    ],
)
@pytest.mark.asyncio
async def test_person_search(
    es_write_data, make_get_request, bulk_query, query_data, expected_answer
):

    bulk_query = bulk_query("persons", PERSON_DATA)
    await es_write_data(SCHEMA, "persons", bulk_query)
    await asyncio.sleep(1)

    response = await make_get_request(API_PERSON_SEARCH, query_data)
    assert response[1] == expected_answer["status"]
    assert len(response[0]) == expected_answer["length"]


@pytest.mark.parametrize(
    "person_id, status, template_answer",
    [
        (
            "009b7728-949e-4250-b9d0-690d97c6a86b",
            200,
            {
                "id": "009b7728-949e-4250-b9d0-690d97c6a86b",
                "full_name": "Rick Austin",
                "films": [
                    {"id": "62bb2379-5017-421a-9030-1f3f7bb51c9c", "roles": ["writer"]}
                ],
            },
        ),
        ("asdf45345353tgdfg", 404, {"detail": "Person not found"}),
    ],
)
@pytest.mark.asyncio
async def test_person_detail(
    es_write_data, make_get_request, bulk_query, person_id, status, template_answer
):
    bulk_query = bulk_query("persons", PERSON_DATA)
    await es_write_data(SCHEMA, "persons", bulk_query)
    await asyncio.sleep(1)

    response = await make_get_request(API_PERSON_DETAIL + person_id)

    assert response[1] == status
    assert response[0] == template_answer


@pytest.mark.parametrize(
    "person_id, status, template_answer",
    [
        (
            "5c360057-c51f-4376-bdf5-049b87fa853b",
            200,
            [
                {
                    "id": "fda827f8-d261-4c23-9e9c-e42787580c4d",
                    "title": "A Star Is Born",
                    "imdb_rating": 7.7,
                }
            ],
        ),
        ("asdf45345353tgdfg", 404, {"detail": "Films for person not found"}),
    ],
)
@pytest.mark.asyncio
async def test_person_film(
    es_write_data, make_get_request, bulk_query, person_id, status, template_answer
):
    bulk_query_persons = bulk_query("persons", PERSON_DATA)
    bulk_query_movies = bulk_query("movies", FILM_DATA)
    schema_movies = load_schema("movies")

    await es_write_data(SCHEMA, "persons", bulk_query_persons)
    await es_write_data(schema_movies, "movies", bulk_query_movies)
    await asyncio.sleep(1)

    response = await make_get_request(API_PERSON_DETAIL + person_id + "/film")

    assert response[1] == status
    assert response[0] == template_answer


@pytest.mark.parametrize(
    "query_data, length",
    [
        (
            {"query": "Star", "page_number": 1, "page_size": 2},
            1,
        ),
        (
                {"query": "Nick"},
                22
        ),
    ],
)
@pytest.mark.asyncio
async def test_person_search_cache(
    es_write_data,
    es_client,
    make_get_request,
    bulk_query,
    query_data,
    length,
    redis,
):
    bulk_query = bulk_query("persons", PERSON_DATA)
    await es_write_data(SCHEMA, "persons", bulk_query)
    await asyncio.sleep(1)

    response_1 = await make_get_request(API_PERSON_SEARCH, query_data)
    redis_keys = await redis.keys("*")

    assert len(redis_keys) == length

    await es_client.indices.delete(index="persons")
    response_2 = await make_get_request(API_PERSON_SEARCH, query_data)

    assert len(response_1[0]) == len(response_2[0])


@pytest.mark.parametrize(
    "person_id, key, length",
    [
        (
            "b0512200-47d3-4128-88fe-4a1356c68c7d",
            "persons:b0512200-47d3-4128-88fe-4a1356c68c7d:detail",
            1,
        ),
    ],
)
@pytest.mark.asyncio
async def test_person_detail_cache(
    es_write_data,
    es_client,
    make_get_request,
    bulk_query,
    key,
    person_id,
    length,
    redis,
):
    bulk_query = bulk_query("persons", PERSON_DATA)
    await es_write_data(SCHEMA, "persons", bulk_query)
    await asyncio.sleep(1)

    response_1 = await make_get_request(API_PERSON_DETAIL + person_id, query_data=None)
    redis_keys = await redis.keys("*")

    assert len(redis_keys) == length
    assert key == redis_keys[0]

    await es_client.indices.delete(index="persons")

    response_2 = await make_get_request(API_PERSON_DETAIL + person_id, query_data=None)

    assert response_1[0] == response_2[0]


@pytest.mark.parametrize(
    "person_id, key, length",
    [
        (
            "5c360057-c51f-4376-bdf5-049b87fa853b",
            "persons:5c360057-c51f-4376-bdf5-049b87fa853b:film:0",
            1,
        ),
    ],
)
@pytest.mark.asyncio
async def test_person_film_cache(
    es_write_data,
    es_client,
    make_get_request,
    bulk_query,
    key,
    person_id,
    length,
    redis,
):
    bulk_query_persons = bulk_query("persons", PERSON_DATA)
    bulk_query_movies = bulk_query("movies", FILM_DATA)
    schema_movies = load_schema("movies")

    await es_write_data(SCHEMA, "persons", bulk_query_persons)
    await es_write_data(schema_movies, "movies", bulk_query_movies)
    await asyncio.sleep(1)

    response_1 = await make_get_request(API_PERSON_DETAIL + person_id + "/film")
    redis_keys = await redis.keys("*")

    assert len(redis_keys) == length
    assert key == redis_keys[0]

    await es_client.indices.delete(index="persons")

    response_2 = await make_get_request(API_PERSON_DETAIL + person_id + "/film")

    assert response_1[0] == response_2[0]
