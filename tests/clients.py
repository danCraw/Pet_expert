import pytest

from app.api.routes.clients import create_client, one_client, delete_client, update_client, add_hospital_to_favourite, \
    favorite_hospitals
from app.models.client import ClientIn, ClientOut
from app.models.favorite_hospital import FavouriteHospital
from app.models.hospital import HospitalIn, HospitalOut
from tests.db.clients.data import db_client
from tests.db.hospitals.data import db_hospital
from tests.db.connection import db_connection
from tests.hospitals import hospital

@pytest.fixture
def client() -> ClientIn:
    return ClientIn(id='1',
                    name='name',
                    password="password",
                    surname='surname',
                    patronomic="patronomic",
                    photo="path",
                    phone="8-800-000-00-00",
                    email="email",
                    )


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
