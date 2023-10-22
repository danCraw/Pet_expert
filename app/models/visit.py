from datetime import date
from typing import Optional

from app.models.base import BaseSchema


class VisitBase(BaseSchema):
    diagnosis: str
    client_id: int
    photos: list[str]
    date_of_receipt: date
    pet_name: str
    pet_age: int
    pet_breed: str
    pet_type: str


class VisitIn(VisitBase):
    id: Optional[int]


class VisitOut(VisitBase):
    id: int
