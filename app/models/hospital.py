from typing import Optional

from app.models.base import BaseSchema


class HospitalBase(BaseSchema):
    name: str
    description: str
    photos: list[str]
    phone: str
    email: str
    password: Optional[str]
    approved: bool
    rating: float


class HospitalIn(HospitalBase, extra='allow'):
    id: Optional[int]


class HospitalOut(HospitalBase):
    id: int

    class Config:
        fields = {
            'some_flag': {
                'exclude': {'password'}
            }
        }


