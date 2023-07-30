from app.models.base import BaseSchema


class FavouriteHospital(BaseSchema):
    hospital_id: int
    client_id: int
