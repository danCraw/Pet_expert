from datetime import datetime
from typing import Optional

from app.models.base import BaseSchema


class HospitalBase(BaseSchema):
    name: str
    description: str
    photos: list[str]
    date_of_receipt: datetime
    phone: str
    email: str
    password_hash: str


class HospitalIn(HospitalBase):
    hospital_id: Optional[int]


class HospitalOut(HospitalBase):
    hospital_id: int

