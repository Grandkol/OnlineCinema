import time

from redis.asyncio import Redis

if __name__ == '__main__':
    # redis = Redis(6379=test_settings.redis_host, port=test_settings.redis_port)
    redis = Redis(host='redis', port="6379")
    while True:
        if redis.ping():
            break
        time.sleep(1)