import pytest_asyncio

from app.api.routes.replies import create_reply, delete_reply
from app.models.reply import ReplyIn, ReplyOut


@pytest_asyncio.fixture
async def db_reply(db_connection, reply: ReplyIn):
    reply: ReplyOut = await create_reply(reply)
    yield reply
    await delete_reply(reply.id)
