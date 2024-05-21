import pytest_asyncio

from app.api.routes.reviews import delete_review, create_review
from app.models.review.base import ReviewIn, ReviewOut


@pytest_asyncio.fixture
async def db_review(db_connection, db_hospital, db_doctor, db_visit, review: ReviewIn):
    review: ReviewOut = await create_review(review)
    yield review
    await delete_review(review.id)
