from typing import Type

import sqlalchemy
from app.db.tables.hospitals import Hospital

from app.db.repositories.base import BaseRepository
from app.models.hospital import HospitalOut, HospitalIn


class HospitalRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return Hospital

    @property
    def _schema_out(self) -> Type[HospitalOut]:
        return HospitalOut

    @property
    def _schema_in(self) -> Type[HospitalIn]:
        return HospitalIn
