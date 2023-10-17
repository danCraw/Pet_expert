import pytest

from app.api.routes.clients import create_client, one_client, delete_client, update_client, add_hospital_to_favourite
from app.models.client import ClientIn, ClientOut
from app.models.favorite_hospital import FavouriteHospital
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
