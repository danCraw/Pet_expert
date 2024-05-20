from app.models.base import BaseSchema


class DoctorFilterModel(BaseSchema):
    name: str | None
    surname: str | None
    patronomic: str | None
    city: str | None
