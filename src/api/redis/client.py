import os

from redis.asyncio.client import Redis

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT") or 6379

if not host or not port:
    raise ValueError("REDIS_HOST and REDIS_PORT environment variables are not set!")

not_needed = os.getenv("REDIS_NOT_NEEDED")

try:
    r = Redis(host=host, port=int(port), decode_responses=True)
except Exception as e:
    if not_needed:
        print(
            f"Warning: Could not connect to Redis, but REDIS_NOT_NEEDED is set. Error: {e}"
        )
        r = None  # type: ignore
    else:
        raise ConnectionError(
            f"Could not connect to Redis at {host}:{port}. Error: {e}"
        )
