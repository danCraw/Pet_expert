import pytest

from app.api.routes.reviews import create_review, one_review, delete_review
from app.models.review import ReviewIn, ReviewOut
from tests.db.connection import db_connection
from tests.db.hospitals.data import db_hospital
from tests.db.doctors.data import db_doctor
from tests.db.visits.data import db_visit
from tests.db.clients.data import db_client
from tests.db.reviews.data import db_review
from tests.test_models import review
from tests.test_models import hospital
from tests.test_models import doctor
from tests.test_models import visit
from tests.test_models import client


@pytest.mark.asyncio
async def test_create(db_connection, db_hospital, db_doctor, db_visit, db_client, review: ReviewIn):
    response: ReviewOut = await create_review(review)
    assert response == ReviewOut(**review.dict())


@pytest.mark.asyncio
async def test_read(db_review: ReviewIn):
    response = await one_review(db_review.id)
    assert response == ReviewOut(**db_review.dict())


@pytest.mark.asyncio
async def test_delete(db_connection, db_hospital, db_doctor, db_visit, db_client, review: ReviewIn):
    await create_review(review)
    response = await delete_review(review.id)
    assert response == ReviewOut(**review.dict())
