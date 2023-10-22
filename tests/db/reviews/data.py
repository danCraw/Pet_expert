import pytest_asyncio

from app.api.routes.reviews import delete_review, create_review
from app.models.review import ReviewIn, ReviewOut
from tests.db.hospitals.data import db_hospital
from tests.db.doctors.data import db_doctor
from tests.db.visits.data import db_visit


@pytest_asyncio.fixture
async def db_review(db_connection, db_hospital, db_doctor, db_visit, review: ReviewIn):
    review: ReviewOut = await create_review(review)
    yield review
    await delete_review(review.id)
