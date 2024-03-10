from pydantic import BaseModel

from app.models.client import ClientUpdate
from app.models.favorite_doctor import FavouriteDoctor
from app.models.favorite_hospital import FavouriteHospital


class Token(BaseModel):
    token: str


class UpdateClient(Token):
    update_data: ClientUpdate


class IdClient(Token):
    id: int


class AddHospitalToFavouriteClient(Token):
    favourite_hospital: FavouriteHospital


class FavouriteDoctorClient(Token):
    favourite_doctor: FavouriteDoctor
