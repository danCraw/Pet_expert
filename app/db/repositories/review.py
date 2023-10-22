import datetime
from typing import Type, Union

import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.reply import ReplyRepository
from app.db.tables.doctors import Doctor
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

    async def create(self,
                     values: Union[ReviewIn, dict],
                     visits_table: Visit,
                     doctors_table: Doctor,
                     hospitals_table: Hospital,
                     ) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = dict(values.dict(exclude_none=True))
        result = await self._db.execute(query=self._table
                                        .insert()
                                        .values(dict_values)
                                        .returning(self._table.c[0]))
        date_of_receipt = await self._db.fetch_val(query=visits_table
                                                   .select()
                                                   .where(visits_table.c.id == values.visit_id)
                                                   .with_only_columns(visits_table.c.date_of_receipt))
        hospital_name = await self._db.fetch_val(query=hospitals_table
                                                 .select()
                                                 .where(hospitals_table.c.id == values.hospital_id)
                                                 .with_only_columns(hospitals_table.c.name))
        doctor_name = await self._db.fetch_val(query=doctors_table
                                               .select()
                                               .where(doctors_table.c.id == values.doctor_id)
                                               .with_only_columns(doctors_table.c.name))
        dict_values.update({self._table.c[0].description: result,
                            'date_of_receipt': date_of_receipt,
                            'hospital_name': hospital_name,
                            'doctor_name': doctor_name,
                            })
        return self._schema_out(**dict_values)

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
