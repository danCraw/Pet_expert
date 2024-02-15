import aioredis

from app.api.exeptions import NotAuthorizedError
from app.redis.base import get_redis


def authorize_client(func):
    async def wrapper(*args, **kwargs):
        client_repo, client = args

        redis: aioredis.Redis = await get_redis()

        client_id = await redis.get(client.token)
        client = await client_repo.get(int(client_id))

        if not client:
            raise NotAuthorizedError()

        return await func(*args, **kwargs)

    return wrapper
