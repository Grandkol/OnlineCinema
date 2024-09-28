import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
    project_name: str = Field("movies", alias="PROJECT_NAME")
    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")

    elastic_host: str = Field("127.0.0.1", alias="ELASTIC_HOST")
    elastic_port: int = Field(9200, alias="ELASTIC_PORT")

    host: str = Field("127.0.0.1", alias="DB_HOST"),
    port: int = Field(5432, alias="DB_PORT"),
    db_name: str = Field("postgres", alies="DB_NAME"),
    user: str = Field("postgres", alies="DB_USER"),
    password: str = Field("123", alies="POSTGRES_PASSWORD"),

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


settings = Settings()
