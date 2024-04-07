import aioredis
import functools

from app.api.exeptions import NotAuthorizedError
from app.core.config import config
from app.db.repositories.admin import AdminRepository
from app.db.repositories.client import ClientRepository
from app.redis.base import get_redis


def client(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        client_repo = ClientRepository()
        token = args[0].token

        if config.IS_TEST:
            return await func(*args, **kwargs)

        admin_repo = AdminRepository()

        redis: aioredis.Redis = await get_redis()

        id_ = await redis.get(token)

        if not id_:
            raise NotAuthorizedError()

        admin = await admin_repo.get(int(id_))

        if not admin:
            client = await client_repo.get(int(id_))

        if not (admin or client):
            raise NotAuthorizedError()

        return await func(*args, **kwargs)

    return wrapper
