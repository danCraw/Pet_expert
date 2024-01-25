from typing import Type

import sqlalchemy

from app.db.repositories.review import ReviewRepository
from app.db.tables.clients import clients
from app.db.tables.doctors import doctors

from app.db.repositories.base import BaseRepository
from app.db.tables.hospitals import hospitals
from app.db.tables.reviews import reviews
from app.db.tables.visits import visits
from app.models.doctor import DoctorOut, DoctorIn


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
                          review_repo: ReviewRepository,
                          ):
        rows = await review_repo._db.fetch_all(
            review_repo.table.select()
        .join(visits, reviews.c.visit_id == visits.c.id, isouter=True)
        .join(self.table, reviews.c.doctor_id == self.table.c.id, isouter=True)
        .join(hospitals, reviews.c.hospital_id == hospitals.c.id, isouter=True)
        .where(reviews.c.doctor_id == doctor_id)
        .with_only_columns(
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
        ))
        return [review_repo._schema_out(**dict(row)) for row in rows] if rows else rows
