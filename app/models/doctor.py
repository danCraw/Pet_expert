from typing import Optional

from app.models.base import BaseSchema


class DoctorBase(BaseSchema):
    name: str
    surname: str
    patronomic: str
    photo: str
    email: str
    password: Optional[str]
    rating: float
    education: str
    treatment_profile: str
    work_experience: float


class DoctorIn(DoctorBase, extra='allow'):
    doctor_id: Optional[int]


class DoctorOut(DoctorBase):
    doctor_id: int

    class Config:
        fields = {
            'some_flag': {
                'exclude': {'password'}
            }
        }