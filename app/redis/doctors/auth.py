import aioredis
import functools

from app.api.exeptions import NotAuthorizedError
from app.core.config import config
from app.db.repositories.admin import AdminRepository
from app.redis.base import get_redis


def doctor(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        doctor_repo = kwargs["doctor_repo"]
        doctor = kwargs["doctor"]

        if config.IS_TEST:
            return await func(*args, **kwargs)

        admin_repo = AdminRepository()

        redis: aioredis.Redis = await get_redis()

        id_ = await redis.get(doctor.token)

        admin = await admin_repo.get(int(id_))

        if not admin:
            doctor = await doctor_repo.get(int(id_))

        if not (doctor or admin):
            raise NotAuthorizedError()

        return await func(*args, **kwargs)

    return wrapper
