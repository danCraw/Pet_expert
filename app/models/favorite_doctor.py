from app.models.base import BaseSchema


class FavouriteDoctor(BaseSchema):
    doctor_id: int
    client_id: int
