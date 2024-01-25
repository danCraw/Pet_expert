from datetime import datetime

import pytest

from app.api.routes.clients import create_client, one_client, delete_client, update_client, add_hospital_to_favourite, \
    favorite_hospitals, add_doctor_to_favourite, favorite_doctors, client_reviews
from app.models.client import ClientIn, ClientOut
from app.models.doctor import DoctorIn, DoctorOut
from app.models.favorite_doctor import FavouriteDoctor
from app.models.favorite_hospital import FavouriteHospital
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
async def test_create(db_connection, client: ClientIn):
    response: ClientOut = await create_client(client)
    assert response == ClientOut(**client.dict())


@pytest.mark.asyncio
async def test_read(db_client: ClientIn):
    response = await one_client(db_client.id)
    assert response == ClientOut(**db_client.dict())


@pytest.mark.asyncio
async def test_update(db_client: ClientIn):
    updated_client = ClientIn(
        id='1',
        name='update_name',
        password="update_password",
        surname='update_surname',
        patronomic="update_patronomic",
        photo="update_path",
        phone="8-800-000-00-11",
        email="update_email",
    )
    client_after_update = await update_client(updated_client)
    updated_client.password_hash = str(hash(updated_client.password))
    assert client_after_update == ClientOut(**updated_client.dict())


@pytest.mark.asyncio
async def test_delete(db_connection, client: ClientIn):
    await create_client(client)
    response = await delete_client(client.id)
    assert response == ClientOut(**client.dict())


@pytest.mark.asyncio
async def test_add_hospital_to_favourite(db_client: ClientIn, db_hospital: HospitalIn):
    test_favourite_hospital = FavouriteHospital(hospital_id=db_hospital.id, client_id=db_client.id)
    response = await add_hospital_to_favourite(test_favourite_hospital)
    assert response == test_favourite_hospital

    test_favorite_hospitals = await favorite_hospitals(client_id=db_client.id)
    assert test_favorite_hospitals == [HospitalOut(**db_hospital.dict())]


@pytest.mark.asyncio
async def test_add_doctor_to_favourite(db_client: ClientIn, db_doctor: DoctorIn):
    test_favourite_doctor = FavouriteDoctor(doctor_id=db_doctor.id, client_id=db_client.id)
    response = await add_doctor_to_favourite(test_favourite_doctor)
    assert response == test_favourite_doctor

    test_favorite_doctors = await favorite_doctors(client_id=db_client.id)
    assert test_favorite_doctors == [DoctorOut(**db_doctor.dict())]


@pytest.mark.asyncio
async def test_client_reviews(db_client: ClientIn, db_review: ReviewIn):
    test_client_reviews = await client_reviews(db_client.id)
    db_review.visit_id = None
    db_review.doctor_id = None
    db_review.hospital_id = None
    assert test_client_reviews == [ReviewOut(**db_review.dict() |
                                                {
                                                'client_name': 'name',
                                                'client_surname': 'surname',
                                                'hospital_name': 'name',
                                                'doctor_name': 'name',
                                                'date_of_receipt': datetime.date(datetime.now())
                                                })]
