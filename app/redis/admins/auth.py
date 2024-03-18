import aioredis
import functools

from app.api.exeptions import NotAuthorizedError
from app.core.config import config
from app.db.repositories.admin import AdminRepository
from app.redis.base import get_redis


def admin(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        token = args[0].token

        if config.IS_TEST:
            return await func(*args, **kwargs)

        admin_repo = AdminRepository()

        redis: aioredis.Redis = await get_redis()

        id_ = await redis.get(token)

        admin = await admin_repo.get(int(id_))

        if not admin:
            raise NotAuthorizedError()

        return await func(*args, **kwargs)

    return wrapper
