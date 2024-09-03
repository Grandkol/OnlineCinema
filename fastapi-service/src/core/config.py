import os
from logging import config as logging_config
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

from core.logger import LOGGING

# load_dotenv('../../../.env')
# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

class Settings(BaseSettings):
    # Настройки Redis
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    # Настройки Elasticsearch
    # elastic_schema: str = Field('http://', env="ELASTIC_SCHEMA")
    elastic_host: str = Field("127.0.0.1", env="ELASTIC_HOST")
    elastic_port: int = Field(9200, env="ELASTIC_PORT")

    # Корень проекта
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = Settings()