import pytest

from app.api.routes.replies import create_reply, review_replies
from app.models.reply import ReplyIn, ReplyOut
from app.models.review import ReviewIn
from tests.db.connection import db_connection
from tests.db.reviews.data import db_review
from tests.db.replies.data import db_reply
from tests.db.hospitals.data import db_hospital
from tests.db.doctors.data import db_doctor
from tests.db.visits.data import db_visit
from tests.db.clients.data import db_client
from tests.test_models import review
from tests.test_models import reply
from tests.test_models import hospital
from tests.test_models import visit
from tests.test_models import doctor
from tests.test_models import client


@pytest.mark.asyncio
async def test_create(db_connection, db_review: ReviewIn, reply: ReplyIn):
    response: ReplyOut = await create_reply(reply)
    assert response == ReplyOut(**reply.dict())


@pytest.mark.asyncio
async def test_review_replies(db_connection, db_review: ReviewIn, db_reply: ReplyIn):
    replies: list[ReplyOut] = await review_replies(db_reply.id)
    assert replies == [ReplyOut(**db_reply.dict())]
