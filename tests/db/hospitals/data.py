import pytest_asyncio

from app.api.routes.hospitals import delete_hospital, create_hospital
from app.models.hospital import HospitalIn, HospitalOut
from tests.hospitals import hospital
from tests.db.connection import db_connection


@pytest_asyncio.fixture
async def db_hospital(db_connection, hospital: HospitalIn):
    hospital: HospitalOut = await create_hospital(hospital)
    yield hospital
    await delete_hospital(hospital.id)
