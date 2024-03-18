from typing import Type

import sqlalchemy
from sqlalchemy import select

from app.db.tables.clients import clients
from app.db.tables.doctors import doctors

from app.db.repositories.base import BaseRepository
from app.db.tables.hospitals import hospitals
from app.db.tables.reviews import reviews
from app.db.tables.visits import visits
from app.models.doctor.base import DoctorOut, DoctorIn
from app.models.review import ReviewOut


class DoctorRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return doctors

    @property
    def _schema_out(self) -> Type[DoctorOut]:
        return DoctorOut

    @property
    def _schema_in(self) -> Type[DoctorIn]:
        return DoctorIn

    async def get_reviews(self,
                          doctor_id: int,
                          ):
        query = select(
            clients.c.name.label('client_name'),
            clients.c.surname.label('client_surname'),
            hospitals.c.name.label('hospital_name'),
            self.table.c.name.label('doctor_name'),
            visits.c.date_of_receipt,
            reviews.c.id,
            reviews.c.liked,
            reviews.c.did_not_liked,
            reviews.c.comment,
            reviews.c.review_time,
            reviews.c.confirmed,
        )
        query = query.join(
            reviews,
            reviews.c.doctor_id == self.table.c.id,
            isouter=True
        )
        query = query.join(
            visits,
            reviews.c.visit_id == visits.c.id,
            isouter=True
        )
        query = query.join(
            hospitals,
            reviews.c.hospital_id == hospitals.c.id,
            isouter=True
        )
        query = query.where(
            self.table.c.id == doctor_id
        )
        rows = await self._db.fetch_all(query)
        return [ReviewOut(**dict(row)) for row in rows] if rows else rows
