import pytest

from app.models.hospital import HospitalIn


@pytest.fixture
def hospital() -> HospitalIn:
    return HospitalIn(id='1',
                      name='name',
                      description='description',
                      photos=['photos_path', ],
                      phone='phone',
                      email='email',
                      password="password"
                      )
