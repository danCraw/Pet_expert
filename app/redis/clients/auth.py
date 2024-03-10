import aioredis
import functools

from app.api.exeptions import NotAuthorizedError
from app.core.config import config
from app.db.repositories.admin import AdminRepository
from app.redis.base import get_redis


def client(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        client_repo = kwargs["client_repo"]
        client = kwargs["client"]
        admin_repo = AdminRepository()

        redis: aioredis.Redis = await get_redis()

        id_ = await redis.get(client.token)

        if config.IS_TEST:
            return await func(*args, **kwargs)

        if not id_:
            raise NotAuthorizedError()

        admin = await admin_repo.get(int(id_))

        if not admin:
            client = await client_repo.get(int(id_))

        if not (client or admin):
            raise NotAuthorizedError()

        return await func(*args, **kwargs)

    return wrapper
