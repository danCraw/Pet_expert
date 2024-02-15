from datetime import datetime, timedelta

import aioredis

from app.core.config import config

import jwt

from app.models.client import ClientIn
from app.redis.base import get_redis


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def create_client_access_token(client: ClientIn) -> str:

    redis: aioredis.Redis = await get_redis()

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": client.name},
        expires_delta=access_token_expires
    )

    await redis.set(access_token, client.id)

    return access_token
