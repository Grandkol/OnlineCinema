import time
import asyncio
from redis.asyncio import Redis

async def ping_redis():
    redis = Redis(host='redis', port="6379")
    while True:
            if await redis.ping():
                break
            await asyncio.sleep(1)

if __name__ == '__main__':
    # redis = Redis(6379=test_settings.redis_host, port=test_settings.redis_port)
    asyncio.run(ping_redis())