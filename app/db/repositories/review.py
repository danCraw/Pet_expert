from typing import Type

import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.reply import ReplyRepository
from app.db.tables.hospitals import Hospital
from app.db.tables.reviews import Review
from app.db.tables.visits import Visit
from app.models.reply import ReplyBase
from app.models.review import ReviewOut, ReviewIn


class ReviewRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _table(self) -> sqlalchemy.Table:
        return Review

    @property
    def _schema_out(self) -> Type[ReviewOut]:
        return ReviewOut

    @property
    def _schema_in(self) -> Type[ReviewIn]:
        return ReviewIn

    async def get_doctor_reviews(self, doctor_id: int, doctors_repo: DoctorRepository, hospitals_table: Hospital, visits_table: Visit):
        rows = await self._db.fetch_all(self._table.select()
                .join(doctors_repo._table, self._table.c.doctor_id == doctors_repo._table.c.doctor_id, isouter=True)
                .join(hospitals_table, self._table.c.hospital_id == hospitals_table.c.hospital_id, isouter=True)
                .join(visits_table, self._table.c.doctor_id == visits_table._table.c.id, isouter=True)
                .where(doctors_repo._table.c.doctor_id == doctor_id)
                .with_only_columns(
                    self._table.c.review_id,
                    self._table.c.client_name,
                    visits_table.c.pet_name,
                    self._table.c.like,
                    self._table.c.did_not_like,
                    self._table.c.comment,
                    self._table.c.review_time,
                    hospitals_table.c.name
                ))
        return [self._schema_out(**dict(dict(row).items())) for row in rows] if rows else rows

    async def reply(self, review_id: int, review: ReviewIn, reply_repo: ReplyRepository):
        reply_review = self.create(review)
        reply_repo.create(ReplyBase(review_id, reply_review.id))
        return reply_review
