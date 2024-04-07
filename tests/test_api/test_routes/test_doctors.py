from datetime import datetime
from typing import Any

import pytest

from app.api.routes.doctors import register_doctor, one_doctor, update_doctor, doctor_reviews
from app.models.auth.doctor import UpdateDoctor
from app.models.doctor.base import DoctorIn, DoctorOut
from app.models.review import ReviewOut, ReviewIn
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

TOKEN = "test_token"


@pytest.mark.asyncio
async def test_create(db_connection, doctor):
    response: dict[str, str | Any] = await register_doctor(doctor)
    assert response.get('access_token') is not None
    assert response['doctor'] == DoctorOut(**doctor.dict())


@pytest.mark.asyncio
async def test_read(db_doctor: DoctorIn):
    response = await one_doctor(db_doctor.id)
    assert response == DoctorOut(**db_doctor.dict())


@pytest.mark.asyncio
async def test_doctor_reviews(db_doctor: DoctorIn, db_review: ReviewIn):
    test_doctor_reviews = await doctor_reviews(db_doctor.id)
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


@pytest.mark.asyncio
async def test_update(db_doctor: DoctorIn):
    updated_doctor = DoctorIn(id='1',
                              name='update_name',
                              surname='update_surname',
                              patronomic='update_patronomic',
                              photo='update_photo',
                              email='update_email',
                              password='update_password',
                              rating=2.1,
                              education='update_education',
                              treatment_profile='update_treatment_profile',
                              work_experience=2.1,
                              approved=False,
                              )
    doctor = UpdateDoctor(update_data=updated_doctor, token=TOKEN)
    doctor_after_update = await update_doctor(doctor)
    updated_doctor.password_hash = str(hash(updated_doctor.password))
    updated_doctor.password = None
    assert doctor_after_update == DoctorOut(**updated_doctor.dict())
