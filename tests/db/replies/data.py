import pytest_asyncio

from app.api.routes.replies import create_reply, delete_reply
from app.models.reply import ReplyIn, ReplyOut


@pytest_asyncio.fixture
async def db_reply(db_connection, doctor_reply: ReplyIn):
    pass
    reply_out: ReplyOut = await create_reply(doctor_reply)
    yield reply_out
    await delete_reply(reply_out.id)
