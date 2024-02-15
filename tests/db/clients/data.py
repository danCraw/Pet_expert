import pytest_asyncio

from app.api.routes.clients import auth_client, delete_client
from app.api.routes.hospitals import delete_hospital, create_hospital
from app.models.client import ClientIn, ClientOut
from app.models.hospital import HospitalIn, HospitalOut


@pytest_asyncio.fixture
async def db_client(db_connection, client: ClientIn):
    client: ClientOut = await auth_client(client)
    yield client
    await delete_client(client.id)


@pytest_asyncio.fixture
async def db_client(db_connection, client: ClientIn):
    client: ClientOut = await auth_client(client)
    yield client
    await delete_client(client.id)


@pytest_asyncio.fixture
async def db_hospital(db_connection, hospital: HospitalIn):
    hospital: HospitalOut = await create_hospital(hospital)
    yield hospital
    await delete_hospital(hospital.id)
