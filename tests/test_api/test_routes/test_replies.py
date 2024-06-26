import pytest

from app.api.routes.replies import create_client_reply, create_doctor_reply, review_replies, delete_doctor_reply, \
    delete_client_reply
from app.models.auth.base import IdModel
# from app.models.auth.base import IdModel
from app.models.auth.reply import CreateReply
from app.models.reply import ReplyIn, ReplyOut
from app.models.review.base import ReviewIn
from tests.db.connection import db_connection
from tests.db.reviews.data import db_review
from tests.db.replies.data import db_reply
from tests.db.hospitals.data import db_hospital
from tests.db.doctors.data import db_doctor
from tests.db.visits.data import db_visit
from tests.db.clients.data import db_client
from tests.test_models import review
from tests.test_models import client_reply, doctor_reply
from tests.test_models import hospital
from tests.test_models import visit
from tests.test_models import doctor
from tests.test_models import client


TOKEN = "test_token"


@pytest.mark.asyncio
async def test_create_client_reply(db_connection, db_review: ReviewIn, client_reply):
    reply = CreateReply(token=TOKEN, reply=client_reply)
    response: ReplyOut = await create_client_reply(reply)
    assert response == ReplyOut(**client_reply.dict())


@pytest.mark.asyncio
async def test_create_doctor_reply(db_connection, db_review: ReviewIn, doctor_reply):
    reply = CreateReply(token=TOKEN, reply=doctor_reply)
    response: ReplyOut = await create_doctor_reply(reply)
    assert response == ReplyOut(**doctor_reply.dict())


@pytest.mark.asyncio
async def test_delete_client_reply(db_connection, db_review: ReviewIn, db_reply: ReplyIn):
    delete_reply = IdModel(id=db_reply.id, token=TOKEN)
    response: ReplyOut = await delete_client_reply(delete_reply)
    replies: list[ReplyOut] = await review_replies(db_reply.id)
    assert replies == []
    assert response == ReplyOut(**db_reply.dict())


@pytest.mark.asyncio
async def test_delete_doctor_reply(db_connection, db_review: ReviewIn, db_reply: ReplyIn):
    delete_reply = IdModel(id=db_reply.id, token=TOKEN)
    response: ReplyOut = await delete_doctor_reply(delete_reply)
    replies: list[ReplyOut] = await review_replies(db_reply.id)
    assert replies == []
    assert response == ReplyOut(**db_reply.dict())


@pytest.mark.asyncio
async def test_review_replies(db_connection, db_review: ReviewIn, db_reply: ReplyIn):
    replies: list[ReplyOut] = await review_replies(db_reply.id)
    assert replies == [ReplyOut(**db_reply.dict())]
