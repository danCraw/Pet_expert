from typing import Any

import pytest_asyncio

from app.api.routes.clients import auth_client, delete_client, register_client
from app.api.routes.hospitals import delete_hospital, create_hospital
from app.models.auth import IdClient
from app.models.client import ClientIn, ClientOut
from app.models.hospital import HospitalIn, HospitalOut


@pytest_asyncio.fixture
async def db_client(db_connection, client: ClientIn):
    result: dict[str, str | Any] = await register_client(client)
    client = result['client']
    yield client
    client = IdClient(token="test_token", id=client.id)
    await delete_client(client=client)


@pytest_asyncio.fixture
async def db_hospital(db_connection, hospital: HospitalIn):
    hospital: HospitalOut = await create_hospital(hospital)
    yield hospital
    await delete_hospital(hospital.id)
