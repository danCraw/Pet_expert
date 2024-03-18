from app.models.client.base import ClientUpdate
from app.models.favorite_doctor import FavouriteDoctor
from app.models.favorite_hospital import FavouriteHospital
from app.models.auth.base import Token


class UpdateClient(Token):
    update_data: ClientUpdate


class AddHospitalToFavouriteClient(Token):
    favourite_hospital: FavouriteHospital


class FavouriteDoctorClient(Token):
    favourite_doctor: FavouriteDoctor
