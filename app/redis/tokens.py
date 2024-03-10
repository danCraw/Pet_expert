from datetime import datetime, timedelta

import aioredis
import jwt

from app.core.config import config
from app.models.base import BaseSchema
from app.redis.base import get_redis


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.TOKEN_SECRET_KEY, algorithm=config.TOKEN_ALGORITHM)
    return encoded_jwt


async def create_access_token(obj: BaseSchema) -> str:
    redis: aioredis.Redis = await get_redis()

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": obj.name},
        expires_delta=access_token_expires
    )

    await redis.set(access_token, obj.id)

    return access_token
