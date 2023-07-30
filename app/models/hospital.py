from datetime import datetime
from typing import Optional

from app.models.base import BaseSchema


class HospitalBase(BaseSchema):
    name: str
    description: str
    photos: list[str]
    phone: str
    email: str
    password: Optional[str]


class HospitalIn(HospitalBase, extra='allow'):
    hospital_id: Optional[int]


class HospitalOut(HospitalBase):
    hospital_id: int

    class Config:
        fields = {
            'some_flag': {
                'exclude': {'password'}
            }
        }


