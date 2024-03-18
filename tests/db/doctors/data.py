from typing import Any

import pytest_asyncio

from app.api.routes.admin import delete_doctor
from app.api.routes.doctors import register_doctor
from app.models.auth.base import IdModel
from app.models.doctor.base import DoctorIn


@pytest_asyncio.fixture
async def db_doctor(db_connection, doctor: DoctorIn):
    result: dict[str, str | Any] = await register_doctor(doctor)
    doctor = result['doctor']
    yield doctor
    model = IdModel(token="test_token", id=doctor.id)
    await delete_doctor(model)
