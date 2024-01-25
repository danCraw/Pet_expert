from datetime import datetime

import pytest

from app.models.client import ClientIn
from app.models.doctor import DoctorIn
from app.models.hospital import HospitalIn
from app.models.reply import ReplyIn
from app.models.review import ReviewIn
from app.models.visit import VisitIn


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


@pytest.fixture
def hospital() -> HospitalIn:
    return HospitalIn(id='1',
                      name='name',
                      description='description',
                      photos=['photos_path', ],
                      phone='phone',
                      email='email',
                      password="password",
                      approved=True
                      )


@pytest.fixture
def review() -> ReviewIn:
    return ReviewIn(id='1',
                    visit_id='1',
                    hospital_id='1',
                    doctor_id='1',
                    client='name surname',
                    liked='liked',
                    did_not_liked='did_not_liked',
                    comment='comment',
                    review_time=datetime.now(),
                    confirmed=True,
                    )


@pytest.fixture
def visit() -> VisitIn:
    return VisitIn(id='1',
                   diagnosis='diagnosis',
                   client_id='1',
                   photos=['photos_path'],
                   date_of_receipt=datetime.date(datetime.now()),
                   pet_name='pet_name',
                   pet_age='1',
                   pet_breed='pet_breed',
                   pet_type='pet_type',
                   )


@pytest.fixture
def reply() -> ReplyIn:
    return ReplyIn(id='1',
                   review_id='1',
                   comment='comment',
                   review_time=datetime.now(),
                   )
