from typing import Type

import sqlalchemy
from app.db.tables.doctors import Doctor

from app.db.repositories.base import BaseRepository
from app.models.doctor import DoctorOut, DoctorIn


class DoctorRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return Doctor

    @property
    def _schema_out(self) -> Type[DoctorOut]:
        return DoctorOut

    @property
    def _schema_in(self) -> Type[DoctorIn]:
        return DoctorIn
