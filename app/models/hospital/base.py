from typing import Optional

from app.models.base import BaseSchema, BaseCredentials


class HospitalBase(BaseSchema):
    name: str
    description: str
    photos: list[str]
    phone: str
    email: str | None
    password: str | None
    approved: bool
    rating: float


class HospitalIn(HospitalBase, extra='allow'):
    id: int | None


class HospitalOut(HospitalBase):
    id: int

    class Config:
        fields = {
            'some_flag': {
                'exclude': {'password'}
            }
        }


class HospitalUpdate(BaseSchema):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    photos: Optional[list[str]]
    phone: Optional[str]
    email: Optional[str]
    password: Optional[str]
    approved: Optional[str]
    rating: Optional[str]
    password_hash: Optional[str]


class HospitalCredentials(BaseCredentials):
    pass
