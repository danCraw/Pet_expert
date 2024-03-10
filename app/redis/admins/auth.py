import aioredis
import functools

from app.api.exeptions import NotAuthorizedError
from app.db.repositories.admin import AdminRepository
from app.redis.base import get_redis


def admin(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get('token')
        admin_repo = AdminRepository()

        redis: aioredis.Redis = await get_redis()

        id_ = await redis.get(token)

        admin = await admin_repo.get(int(id_))

        if not admin:
            raise NotAuthorizedError()

        return await func(*args, **kwargs)

    return wrapper
