from datetime import datetime

import pytest

from app.api.routes.hospitals import create_hospital, delete_hospital, update_hospital, one_hospital, hospital_reviews
from app.models.hospital import HospitalIn, HospitalOut
from app.models.review import ReviewIn, ReviewOut
from tests.db.connection import db_connection
from tests.db.clients.data import db_client
from tests.db.hospitals.data import db_hospital
from tests.db.doctors.data import db_doctor
from tests.db.visits.data import db_visit
from tests.db.reviews.data import db_review
from tests.test_models import client
from tests.test_models import doctor
from tests.test_models import hospital
from tests.test_models import visit
from tests.test_models import review


@pytest.mark.asyncio
async def test_create(db_connection, hospital):
    response: HospitalOut = await create_hospital(hospital)
    assert response == HospitalOut(**hospital.dict())


@pytest.mark.asyncio
async def test_read(db_hospital: HospitalIn):
    response = await one_hospital(db_hospital.id)
    assert response == HospitalOut(**db_hospital.dict())


@pytest.mark.asyncio
async def test_update(db_hospital: HospitalIn):
    updated_hospital = HospitalIn(id='1',
                                  name='update_name',
                                  description='update_description',
                                  photos=['update_photos_path', ],
                                  phone='update_phone',
                                  email='update_email',
                                  password="update_password",
                                  approved=False,
                                  rating=1.1,
                                  )
    hospital_after_update = await update_hospital(updated_hospital)
    updated_hospital.password_hash = str(hash(updated_hospital.password))
    assert hospital_after_update == HospitalOut(**updated_hospital.dict())


@pytest.mark.asyncio
async def test_delete(db_connection, hospital: HospitalIn):
    await create_hospital(hospital)
    response = await delete_hospital(hospital.id)
    assert response == HospitalOut(**hospital.dict())


@pytest.mark.asyncio
async def test_doctor_reviews(db_hospital: HospitalIn, db_review: ReviewIn):
    test_doctor_reviews = await hospital_reviews(db_hospital.id)
    db_review.visit_id = None
    db_review.doctor_id = None
    db_review.hospital_id = None
    assert test_doctor_reviews == [ReviewOut(**db_review.dict() |
                                               {
                                                   'client_name': 'name',
                                                   'client_surname': 'surname',
                                                   'hospital_name': 'name',
                                                   'doctor_name': 'name',
                                                   'date_of_receipt': datetime.date(datetime.now())
                                               })]

