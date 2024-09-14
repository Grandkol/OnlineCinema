from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
    es_host: str = Field("http://elastic:9200", alias="ELASTIC_HOST")
    es_index: str = Field("movies")
    # es_index_mapping: dict = Field("mapping", env="ELASTIC_MAPPING")

    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    service_url: str = Field("http://fastapi:8000/api/v1/", alias="SERVICE_URL")


test_settings = TestSettings()