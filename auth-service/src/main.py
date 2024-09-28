from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from redis.asyncio import Redis

from core.config import settings
from db.postgres import create_database, purge_database
from db.redis_bd import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis(host=settings.redis.host, port=settings.redis.port, db=0, decode_responses=True)
    await create_database()

    yield

    await redis.redis.close()
    await purge_database



app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
