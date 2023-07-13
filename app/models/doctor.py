from typing import Optional

from app.models.base import BaseSchema


class DoctorBase(BaseSchema):
    name: str
    surname: str
    patronomic: str
    photo: str
    email: str
    password_hash: str
    rating: float
    education: str
    treatment_profile: str
    work_experience: str


class DoctorIn(DoctorBase):
    doctor_id: Optional[int]


class DoctorOut(DoctorBase):
    doctor_id: int

