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
    approved: bool


class DoctorIn(DoctorBase, extra='allow'):
    id: Optional[int]


class DoctorOut(DoctorBase):
    id: int

    class Config:
        fields = {
            'some_flag': {
                'exclude': {'password'}
            }
        }


class DoctorUpdate(BaseSchema):
    id: Optional[int]
    name: Optional[str]
    surname: Optional[str]
    patronomic: Optional[str]
    photo: Optional[str]
    email: Optional[str]
    password: Optional[str]
    password_hash: Optional[str]
    rating: Optional[float]
    education: Optional[str]
    treatment_profile: Optional[str]
    work_experience: Optional[float]
    approved: Optional[bool]


class DoctorCredentials(BaseSchema):
    email: str
    password: str
