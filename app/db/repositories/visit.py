from typing import Type

import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.tables.visits import visits
from app.models.visit import VisitOut, VisitIn


class VisitRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return visits

    @property
    def _schema_out(self) -> Type[VisitOut]:
        return VisitOut

    @property
    def _schema_in(self) -> Type[VisitIn]:
        return VisitIn
