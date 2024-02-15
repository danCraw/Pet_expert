import aioredis
from aioredis import Redis

from app.core.config import config


async def get_redis() -> Redis:
    redis = await aioredis.from_url(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    return redis

