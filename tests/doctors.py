import pytest

from app.api.routes.doctors import create_doctor
from app.models.doctor import DoctorIn, DoctorOut
from tests.db.clients.data import db_client
from tests.db.hospitals.data import db_hospital
from tests.db.connection import db_connection
from tests.hospitals import hospital


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
                    )


@pytest.mark.asyncio
async def test_create(db_connection, doctor):
    response: DoctorOut = await create_doctor(doctor)
    assert response == DoctorOut(**doctor.dict())
