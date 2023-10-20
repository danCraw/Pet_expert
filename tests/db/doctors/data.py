import pytest_asyncio

from app.api.routes.doctors import create_doctor, delete_doctor
from app.models.doctor import DoctorIn, DoctorOut


@pytest_asyncio.fixture
async def db_doctor(db_connection, doctor: DoctorIn):
    doctor: DoctorOut = await create_doctor(doctor)
    yield doctor
    await delete_doctor(doctor.id)
