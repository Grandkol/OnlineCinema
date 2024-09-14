from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import pytest_asyncio
import asyncio

import pytest
from functional.settings import test_settings

MAPPING_MOVIES = {
    "settings": {
      "refresh_interval": "1s",
      "analysis": {
        "filter": {
          "english_stop": {
            "type":       "stop",
            "stopwords":  "_english_"
          },
          "english_stemmer": {
            "type": "stemmer",
            "language": "english"
          },
          "english_possessive_stemmer": {
            "type": "stemmer",
            "language": "possessive_english"
          },
          "russian_stop": {
            "type":       "stop",
            "stopwords":  "_russian_"
          },
          "russian_stemmer": {
            "type": "stemmer",
            "language": "russian"
          }
        },
        "analyzer": {
          "ru_en": {
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "english_stop",
              "english_stemmer",
              "english_possessive_stemmer",
              "russian_stop",
              "russian_stemmer"
            ]
          }
        }
      }
    },
    "mappings": {
      "dynamic": "strict",
      "properties": {
        "id": {
          "type": "keyword"
        },
        "imdb_rating": {
          "type": "float"
        },
        "genres": {
          "type": "nested",
          "dynamic": "strict",
          "properties": {
            "id": {
              "type": "keyword"
            },
            "name": {
              "type": "text",
              "analyzer": "ru_en"
            }
          }

        },
        "title": {
          "type": "text",
          "analyzer": "ru_en",
          "fields": {
            "raw": {
              "type":  "keyword"
            }
          }
        },
        "description": {
          "type": "text",
          "analyzer": "ru_en"
        },
        "directors_names": {
          "type": "text",
          "analyzer": "ru_en"
        },
        "actors_names": {
          "type": "text",
          "analyzer": "ru_en"
        },
        "writers_names": {
          "type": "text",
          "analyzer": "ru_en"
        },
        "directors": {
          "type": "nested",
          "dynamic": "strict",
          "properties": {
            "id": {
              "type": "keyword"
            },
            "name": {
              "type": "text",
              "analyzer": "ru_en"
            }
          }
        },
        "actors": {
          "type": "nested",
          "dynamic": "strict",
          "properties": {
            "id": {
              "type": "keyword"
            },
            "name": {
              "type": "text",
              "analyzer": "ru_en"
            }
          }
        },
        "writers": {
          "type": "nested",
          "dynamic": "strict",
          "properties": {
            "id": {
              "type": "keyword"
            },
            "name": {
              "type": "text",
              "analyzer": "ru_en"
            }
          }
        }
      }
    }
  }


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict]):
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(index=test_settings.es_index, **MAPPING_MOVIES)

        updated, errors = await async_bulk(client=es_client, actions=data)

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner
