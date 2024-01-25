from typing import Type, Union

import sqlalchemy
from databases.interfaces import Record
from sqlalchemy import column, true, false

from app.db.repositories.base import BaseRepository
from app.db.tables.clients import clients
from app.db.tables.doctors import doctors
from app.db.tables.hospitals import hospitals
from app.db.tables.reviews import reviews
from app.db.tables.visits import visits
from app.models.review import ReviewOut, ReviewIn


class ReviewRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return reviews

    @property
    def _schema_out(self) -> Type[ReviewOut]:
        return ReviewOut

    @property
    def _schema_in(self) -> Type[ReviewIn]:
        return ReviewIn

    async def _list(self) -> list[Record]:

        query = (self.table.select()
        .join(visits, self.table.c.visit_id == visits.c.id, isouter=True)
        .join(doctors, self.table.c.doctor_id == doctors.c.id, isouter=True)
        .join(hospitals, self.table.c.hospital_id == hospitals.c.id, isouter=True)
        .with_only_columns(
            clients.c.name.label('client_name'),
            clients.c.surname.label('client_surname'),
            hospitals.c.name.label('hospital_name'),
            doctors.c.name.label('doctor_name'),
            visits.c.date_of_receipt,
            self.table.c.id,
            self.table.c.liked,
            self.table.c.did_not_liked,
            self.table.c.comment,
            self.table.c.review_time,
            self.table.c.confirmed))
        return await self._db.fetch_all(query)

    async def list(self) -> list:
        rows = await self._list()
        return [self._schema_out(**dict(row)) for row in rows]

    async def _review_additional_info(self,
                                      client_id: int,
                                      visit_id: int,
                                      doctor_id: int,
                                      hospital_id: int
                                      ):
        client = await self._db.fetch_one(query=clients
                                          .select()
                                          .where(clients.c.id == client_id)
                                          .with_only_columns(clients.c.name,
                                                             clients.c.surname))
        client_name, client_surname = client
        date_of_receipt = await self._db.fetch_val(query=visits
                                                   .select()
                                                   .where(visits.c.id == visit_id)
                                                   .with_only_columns(visits.c.date_of_receipt))
        hospital_name = await self._db.fetch_val(query=hospitals
                                                 .select()
                                                 .where(hospitals.c.id == hospital_id)
                                                 .with_only_columns(hospitals.c.name))
        doctor_name = await self._db.fetch_val(query=doctors
                                               .select()
                                               .where(doctors.c.id == doctor_id)
                                               .with_only_columns(doctors.c.name))
        return client_name, client_surname, date_of_receipt, hospital_name, doctor_name

    async def create(self,
                     values: Union[ReviewIn, dict],
                     ) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = dict(values.dict(exclude_none=True))
        result = await self._db.execute(query=self.table
                                        .insert()
                                        .values(dict_values)
                                        .returning(self.table.c[0]))
        visit = await self._db.fetch_one(query=visits
                                         .select()
                                         .where(visits.c.id == values.visit_id)
                                         )
        client_name, client_surname, date_of_receipt, hospital_name, doctor_name = await self._review_additional_info(
            client_id=dict(visit)['client_id'],
            visit_id=values.visit_id,
            doctor_id=values.doctor_id,
            hospital_id=values.hospital_id,
        )
        dict_values.update(
            dict(
                id=result,
                client_name=client_name,
                client_surname=client_surname,
                date_of_receipt=date_of_receipt,
                hospital_name=hospital_name,
                doctor_name=doctor_name
            )
        )
        return self._schema_out(**dict_values)

    async def get(self,
                  review_id: int,
                  ):
        row = await self._db.fetch_one(query=self.table
        .select()
        .where(
            self.table.c.id == review_id)
        )
        review = dict(row)
        visit = await self._db.fetch_one(query=visits
                                         .select()
                                         .where(visits.c.id == review['visit_id'])
                                         )
        client_name, client_surname, date_of_receipt, hospital_name, doctor_name = await self._review_additional_info(
            client_id=dict(visit)['client_id'],
            visit_id=review['visit_id'],
            doctor_id=review['doctor_id'],
            hospital_id=review['hospital_id'],
        )
        if row:
            return self._schema_out(**dict(row) | {
                'date_of_receipt': date_of_receipt,
                'client_name': client_name,
                'client_surname': client_surname,
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

    async def get_doctor_reviews(self, doctor_id: int, filters: dict):
        query = (self.table
                 .select()
                 .join(doctors, self.table.c.doctor_id == doctors.c.doctor_id, isouter=True)
                 .join(hospitals, self.table.c.hospital_id == hospitals.c.hospital_id, isouter=True)
                 .join(visits, self.table.c.doctor_id == visits.table.c.id, isouter=True))

        if filters:
            if filters.get('confirmed', None) is not None:
                confirmed = true() if filters.get('confirmed') else false()
                query = query.where(reviews.c.confirmed == confirmed)

        rows = await self._db.fetch_all(
            query
            .where(doctors.c.doctor_id == doctor_id)
            .with_only_columns(
                self.table.c.review_id,
                self.table.c.client_name,
                visits.c.pet_name,
                self.table.c.like,
                self.table.c.did_not_like,
                self.table.c.comment,
                self.table.c.review_time,
                hospitals.c.name
            )
        )
        return [self._schema_out(**dict(row)) for row in rows] if rows else rows
