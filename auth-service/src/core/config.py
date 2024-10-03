import os
from logging import config as logging_config
from pathlib import Path

from pydantic import Field, BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"


class DatabaseConfig(BaseSettings):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class RunConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8001


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="AUTH__",
    )
    project_name: str = Field("Auth", alias="PROJECT_NAME")
    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")

    auth_jwt: AuthJWT = AuthJWT()
    run_config: RunConfig = RunConfig()

    db: DatabaseConfig

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


settings = Settings()
print(settings.db.url)