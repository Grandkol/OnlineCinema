from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
    es_host: str = Field("http://127.0.0.1:9200", env="ELASTIC_HOST")
    es_index: str = Field('movies', env="ELASTIC_INDEX")
    es_id_field: str = Field()
    # es_index_mapping: dict = Field("mapping", env="ELASTIC_MAPPING")

    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    service_url: str = Field("http://localhost:8000", env="SERVICE_URL")


test_settings = TestSettings()