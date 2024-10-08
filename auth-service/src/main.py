import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from redis.asyncio import Redis

from core.config import settings
from api.v1 import auth
from db import db_helper
from models import Base
from db.redis_db import redis
from services import redis



@asynccontextmanager
async def lifespan(app: FastAPI):
    print(await redis._get_redis_keys())

    yield

    await db_helper.dispose()

    await redis.close()



app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(roles.router, prefix="/api/v1/roles", tags=["roles"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run_config.host,
        port=settings.run_config.port,
        reload=True,
    )

