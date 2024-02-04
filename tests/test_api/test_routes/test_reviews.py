from datetime import datetime

import pytest
from fastapi import HTTPException

from app.api.routes.reviews import create_review, one_review, delete_review, reviews_list
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.review import ReviewRepository
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
    doctor_repo: DoctorRepository = DoctorRepository()

    review.doctor_assessment = 5
    response: ReviewOut = await create_review(review)
    assert response == ReviewOut(**review.dict() | {'client_name': 'name',
                                                    'client_surname': 'surname',
                                                    'hospital_name': 'name',
                                                    'doctor_name': 'name',
                                                    'date_of_receipt': datetime.date(datetime.now())
                                                    })

    test_doctor = await doctor_repo.get(db_doctor.id)

    assert test_doctor.rating == 5


@pytest.mark.asyncio
async def test_read(db_review: ReviewIn):
    response = await one_review(db_review.id)
    assert response == ReviewOut(**db_review.dict() | {'client_name': 'name',
                                                    'client_surname': 'surname',
                                                    'hospital_name': 'name',
                                                    'doctor_name': 'name',
                                                    'date_of_receipt': datetime.date(datetime.now())
                                                    })


@pytest.mark.asyncio
async def test_list_reviews(db_review: ReviewIn):
    response = await reviews_list()
    db_review.visit_id = None
    db_review.hospital_id = None
    db_review.doctor_id = None
    assert response == [ReviewOut(**db_review.dict() | {'client_name': 'name',
                                                        'client_surname': 'surname',
                                                        'hospital_name': 'name',
                                                        'doctor_name': 'name',
                                                        'date_of_receipt': datetime.date(datetime.now())
                                                        })]


@pytest.mark.asyncio
async def test_delete(db_connection, db_hospital, db_doctor, db_visit, db_client, review: ReviewIn):
    await create_review(review)
    response = await delete_review(review.id)
    assert response == review.id


@pytest.mark.asyncio
async def test_delete_wrong_id(db_connection, db_hospital, db_doctor, db_visit, db_client, review: ReviewIn):
    await create_review(review)
    with pytest.raises(HTTPException):
        await delete_review(2)
