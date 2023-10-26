from typing import Type, Union

import sqlalchemy
from databases.interfaces import Record
from sqlalchemy import column, join

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
    def table(self) -> sqlalchemy.Table:
        return Review

    @property
    def _schema_out(self) -> Type[ReviewOut]:
        return ReviewOut

    @property
    def _schema_in(self) -> Type[ReviewIn]:
        return ReviewIn

    async def _list(self,
                    visits_table: Visit,
                    doctors_table: Doctor,
                    hospitals_table: Hospital,
                    ) -> list[Record]:
        return await self._db.fetch_all(self.table.select()
                     .join(visits_table, self.table.c.visit_id == visits_table.c.id, isouter=True)
                     .join(doctors_table, self.table.c.doctor_id == doctors_table.c.id, isouter=True)
                     .join(hospitals_table, self.table.c.hospital_id == hospitals_table.c.id, isouter=True)
                     .with_only_columns(
                     hospitals_table.c.name.label('hospital_name'),
                     doctors_table.c.name.label('doctor_name'),
                     visits_table.c.date_of_receipt,
                     self.table.c.id,
                     self.table.c.liked,
                     self.table.c.did_not_liked,
                     self.table.c.comment,
                     self.table.c.review_time,
                     self.table.c.confirmed))

    async def list(self,
                   visits_table: Visit,
                   doctors_table: Doctor,
                   hospitals_table: Hospital,
                   ) -> list:
        rows = await self._list(visits_table,
                                doctors_table,
                                hospitals_table,
                                )
        return [self._schema_out(**dict(dict(row).items())) for row in rows]


    async def _review_additional_info(self,
                                      visit_id: int,
                                      doctor_id: int,
                                      hospital_id: int,
                                      visits_table: Visit,
                                      doctors_table: Doctor,
                                      hospitals_table: Hospital,
                                      ):
        date_of_receipt = await self._db.fetch_val(query=visits_table
                                                   .select()
                                                   .where(visits_table.c.id == visit_id)
                                                   .with_only_columns(visits_table.c.date_of_receipt))
        hospital_name = await self._db.fetch_val(query=hospitals_table
                                                 .select()
                                                 .where(hospitals_table.c.id == hospital_id)
                                                 .with_only_columns(hospitals_table.c.name))
        doctor_name = await self._db.fetch_val(query=doctors_table
                                               .select()
                                               .where(doctors_table.c.id == doctor_id)
                                               .with_only_columns(doctors_table.c.name))
        return date_of_receipt, hospital_name, doctor_name

    async def create(self,
                     values: Union[ReviewIn, dict],
                     visits_table: Visit,
                     doctors_table: Doctor,
                     hospitals_table: Hospital,
                     ) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = dict(values.dict(exclude_none=True))
        result = await self._db.execute(query=self.table
                                        .insert()
                                        .values(dict_values)
                                        .returning(self.table.c[0]))
        date_of_receipt, hospital_name, doctor_name = await self._review_additional_info(
                                           values.visit_id,
                                           values.doctor_id,
                                           values.hospital_id,
                                           visits_table,
                                           doctors_table,
                                           hospitals_table
                                           )
        dict_values.update({self.table.c[0].description: result,
                            'date_of_receipt': date_of_receipt,
                            'hospital_name': hospital_name,
                            'doctor_name': doctor_name,
                            })
        return self._schema_out(**dict_values)

    async def get(self,
                  review_id: int,
                  visits_table: Visit,
                  doctors_table: Doctor,
                  hospitals_table: Hospital
                  ):
        row = await self._db.fetch_one(query=self.table.select().where(column(self.table.c[0].description) == review_id))
        review = dict(row)
        date_of_receipt, hospital_name, doctor_name = await self._review_additional_info(
            review['visit_id'],
            review['doctor_id'],
            review['hospital_id'],
            visits_table,
            doctors_table,
            hospitals_table
        )
        if row:
            return self._schema_out(**dict(row) | {'date_of_receipt': date_of_receipt,
                                                   'hospital_name': hospital_name,
                                                   'doctor_name': doctor_name,
                                                   })
        else:
            return row

    async def delete(self, review_id: Union[int, str]) -> _schema_out:
        result = await self._db.execute(query=self.table
                                        .delete()
                                        .where(column(self.table.c[0].description) == review_id)
                                        .returning(self.table.c[0]))
        return result

    async def get_doctor_reviews(self, doctor_id: int, doctors_repo: DoctorRepository, hospitals_table: Hospital, visits_table: Visit):
        rows = await self._db.fetch_all(self.table.select()
                .join(doctors_repo.table, self.table.c.doctor_id == doctors_repo.table.c.doctor_id, isouter=True)
                .join(hospitals_table, self.table.c.hospital_id == hospitals_table.c.hospital_id, isouter=True)
                .join(visits_table, self.table.c.doctor_id == visits_table.table.c.id, isouter=True)
                .where(doctors_repo.table.c.doctor_id == doctor_id)
                .with_only_columns(
                    self.table.c.review_id,
                    self.table.c.client_name,
                    visits_table.c.pet_name,
                    self.table.c.like,
                    self.table.c.did_not_like,
                    self.table.c.comment,
                    self.table.c.review_time,
                    hospitals_table.c.name
                ))
        return [self._schema_out(**dict(dict(row).items())) for row in rows] if rows else rows

    async def reply(self, review_id: int, review: ReviewIn, reply_repo: ReplyRepository):
        reply_review = self.create(review)
        reply_repo.create(ReplyBase(review_id, reply_review.id))
        return reply_review
