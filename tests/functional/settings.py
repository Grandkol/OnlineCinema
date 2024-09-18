from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
    es_host: str = Field("http://172.27.0.5:9200", alias="ELASTIC_HOST")
    es_index: str = Field("movies")
    # es_index_mapping: dict = Field("mapping", env="ELASTIC_MAPPING")

    redis_host: str = Field("111", alias="REDIS_HOST")
    redis_port: int = Field(6379, alies="REDIS_PORT")
    service_url: str = Field("http://127.0.0.1:80/api/v1/", alias="SERVICE_URL")


test_settings = TestSettings()
