from typing import Any

import pytest_asyncio

from app.api.routes.hospitals import delete_hospital, register_hospital
from app.models.auth.base import IdModel
from app.models.hospital.base import HospitalIn


@pytest_asyncio.fixture
async def db_hospital(db_connection, hospital: HospitalIn):
    result: dict[str, str | Any] = await register_hospital(hospital)
    hospital = result['hospital']
    yield hospital
    hospital = IdModel(token="test_token", id=hospital.id)
    await delete_hospital(hospital)
