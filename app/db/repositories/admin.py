from typing import Type

import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.admins import admins
from app.models.admin import AdminOut, AdminIn


class AdminRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return admins

    @property
    def _schema_out(self) -> Type[AdminOut]:
        return AdminOut

    @property
    def _schema_in(self) -> Type[AdminIn]:
        return AdminIn
