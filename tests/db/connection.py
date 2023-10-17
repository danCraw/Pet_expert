import pytest_asyncio

from app.db.base import database


@pytest_asyncio.fixture
async def db_connection():
    await database.connect()
    yield
    await database.disconnect()
