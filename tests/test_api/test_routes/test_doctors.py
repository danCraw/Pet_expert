import pytest

from app.api.routes.doctors import create_doctor, one_doctor, update_doctor, delete_doctor
from app.models.doctor import DoctorIn, DoctorOut
from tests.db.connection import db_connection
from tests.db.doctors.data import db_doctor


@pytest.fixture
def doctor() -> DoctorIn:
    return DoctorIn(id='1',
                    name='name',
                    surname='surname',
                    patronomic='patronomic',
                    photo='photo',
                    email='email',
                    password='password',
                    rating=1.1,
                    education='education',
                    treatment_profile='treatment_profile',
                    work_experience=1.1,
                    approved=True,
                    )


@pytest.mark.asyncio
async def test_create(db_connection, doctor):
    response: DoctorOut = await create_doctor(doctor)
    assert response == DoctorOut(**doctor.dict())


@pytest.mark.asyncio
async def test_read(db_doctor: DoctorIn):
    response = await one_doctor(db_doctor.id)
    assert response == DoctorOut(**db_doctor.dict())


@pytest.mark.asyncio
async def test_update(db_doctor: DoctorIn):
    updated_doctor = DoctorIn(id='1',
                              name='update_name',
                              surname='update_surname',
                              patronomic='update_patronomic',
                              photo='update_photo',
                              email='update_email',
                              password='update_password',
                              rating=2.1,
                              education='update_education',
                              treatment_profile='update_treatment_profile',
                              work_experience=2.1,
                              approved=False
                              )
    doctor_after_update = await update_doctor(updated_doctor)
    updated_doctor.password_hash = str(hash(updated_doctor.password))
    assert doctor_after_update == DoctorOut(**updated_doctor.dict())


@pytest.mark.asyncio
async def test_delete(db_connection, doctor: DoctorIn):
    await create_doctor(doctor)
    response = await delete_doctor(doctor.id)
    assert response == DoctorOut(**doctor.dict())
