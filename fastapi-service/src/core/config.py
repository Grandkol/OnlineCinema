import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from logging import config as logging_config

from .logger import LOGGING


logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')
    project_name: str = Field("movies", alias="PROJECT_NAME")
    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")

    elastic_host: str = Field("127.0.0.1", alias="ELASTIC_HOST")
    elastic_port: int = Field(9200, alias="ELASTIC_PORT")

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


settings = Settings()