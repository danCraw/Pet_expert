from datetime import datetime
from typing import Optional

from app.models.base import BaseSchema


class DoctorServiceBase(BaseSchema):
    doctor_id: int
    service_id: int
    price: int


class DoctorServiceIn(DoctorServiceBase):
    service_id: Optional[int]
    doctor_id: Optional[int]


class DoctorServiceOut(DoctorServiceBase):
    service_id: int
    doctor_id_id: int

