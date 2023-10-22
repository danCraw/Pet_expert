import pytest

from app.api.routes.hospitals import create_hospital, delete_hospital, update_hospital, one_hospital
from app.models.hospital import HospitalIn, HospitalOut
from tests.db.connection import db_connection
from tests.db.hospitals.data import db_hospital
from tests.test_models import hospital


@pytest.mark.asyncio
async def test_create(db_connection, hospital):
    response: HospitalOut = await create_hospital(hospital)
    assert response == HospitalOut(**hospital.dict())


@pytest.mark.asyncio
async def test_read(db_hospital: HospitalIn):
    response = await one_hospital(db_hospital.id)
    assert response == HospitalOut(**db_hospital.dict())


@pytest.mark.asyncio
async def test_update(db_hospital: HospitalIn):
    updated_hospital = HospitalIn(id='1',
                                  name='update_name',
                                  description='update_description',
                                  photos=['update_photos_path', ],
                                  phone='update_phone',
                                  email='update_email',
                                  password="update_password",
                                  approved=False
                                  )
    hospital_after_update = await update_hospital(updated_hospital)
    updated_hospital.password_hash = str(hash(updated_hospital.password))
    assert hospital_after_update == HospitalOut(**updated_hospital.dict())


@pytest.mark.asyncio
async def test_delete(db_connection, hospital: HospitalIn):
    await create_hospital(hospital)
    response = await delete_hospital(hospital.id)
    assert response == HospitalOut(**hospital.dict())
