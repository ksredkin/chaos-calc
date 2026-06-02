import os

from redis.asyncio.client import Redis

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT") or 6379

if not host or not port:
    raise ValueError("REDIS_HOST and REDIS_PORT environment variables are not set!")

r = Redis(host=host, port=int(port), decode_responses=True)
