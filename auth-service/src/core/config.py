import os
from logging import config as logging_config
from pathlib import Path

from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR/"src"/"certs"/"jwt-private.pem"
    public_key_path: Path = BASE_DIR/"src"/"certs"/"jwt-public.pem"
    algorithm: str = "RS256"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
    project_name: str = Field("Auth", alias="PROJECT_NAME")
    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")

    elastic_host: str = Field("127.0.0.1", alias="ELASTIC_HOST")
    elastic_port: int = Field(9200, alias="ELASTIC_PORT")

    # host: str = Field("127.0.0.1", alias="DB_HOST"),
    # port: int = Field(5432, alias="DB_PORT"),
    # db_name: str = Field("postgres", alias="DB_NAME"),
    # user: str = Field("postgres", alias="DB_USER"),
    # password: str = Field("123", alias="POSTGRES_PASSWORD"),
    auth_jwt: AuthJWT = AuthJWT()

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


settings = Settings()
