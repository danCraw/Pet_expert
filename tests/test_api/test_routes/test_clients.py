from datetime import datetime
from typing import Any

import pytest

from app.api.routes.clients import auth_client, delete_client, update_client, add_hospital_to_favourite, \
    favourite_hospitals, add_doctor_to_favourite, favorite_doctors, client_reviews, register_client, one_client
from app.models.auth.base import IdModel
from app.models.auth.client import UpdateClient, AddHospitalToFavouriteClient, FavouriteDoctorClient
from app.models.client.base import ClientIn, ClientOut, ClientCredentials, ClientUpdate
from app.models.doctor.base import DoctorIn, DoctorOut
from app.models.favorite_doctor import FavouriteDoctor
from app.models.favorite_hospital import FavouriteHospital
from app.models.hospital.base import HospitalIn, HospitalOut
from app.models.review.base import ReviewIn, ReviewOut
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
async def test_create(db_connection, client: ClientIn):
    response: dict[str, str | Any] = await register_client(client)
    assert response.get('access_token') is not None
    assert response['client'] == ClientOut(**client.dict())


@pytest.mark.asyncio
async def test_read(db_client: ClientIn):
    response = await one_client(db_client.id)
    assert response == ClientOut(**db_client.dict())


@pytest.mark.asyncio
async def test_auth(db_client: ClientIn):
    credentials = ClientCredentials(email=db_client.email, password='password')
    response = await auth_client(credentials)
    assert response.get('access_token') is not None
    assert response['client'] == ClientOut(**db_client.dict())


@pytest.mark.asyncio
async def test_update(db_client: ClientIn):
    updated_client = ClientUpdate(
        id='1',
        name='update_name',
        password="update_password",
        surname='update_surname',
        patronomic="update_patronomic",
        photo="update_path",
        phone="8-800-000-00-11",
        email="update_email",
    )
    client = UpdateClient(update_data=updated_client, token=TOKEN)
    client_after_update = await update_client(client)
    updated_client.password_hash = str(hash(updated_client.password))
    assert client_after_update == ClientOut(**updated_client.dict())


@pytest.mark.asyncio
async def test_delete(db_connection, client: ClientIn):
    await register_client(client)
    client_delete = IdModel(id=client.id, token=TOKEN)
    response = await delete_client(client_delete)
    assert response == ClientOut(**client.dict())


@pytest.mark.asyncio
async def test_add_hospital_to_favourite(db_client: ClientIn, db_hospital: HospitalIn):
    test_favourite_hospital = FavouriteHospital(hospital_id=db_hospital.id, client_id=db_client.id)
    client = AddHospitalToFavouriteClient(favourite_hospital=test_favourite_hospital, token=TOKEN)
    response = await add_hospital_to_favourite(client)
    assert response == test_favourite_hospital

    id_client = IdModel(id=db_client.id, token=TOKEN)
    test_favorite_hospitals = await favourite_hospitals(id_client)
    assert test_favorite_hospitals == [HospitalOut(**db_hospital.dict())]


@pytest.mark.asyncio
async def test_add_doctor_to_favourite(db_client: ClientIn, db_doctor: DoctorIn):
    test_favourite_doctor = FavouriteDoctor(doctor_id=db_doctor.id, client_id=db_client.id)
    client = FavouriteDoctorClient(favourite_doctor=test_favourite_doctor, token=TOKEN)
    response = await add_doctor_to_favourite(client)
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
