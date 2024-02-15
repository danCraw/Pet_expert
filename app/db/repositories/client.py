from typing import Type

import sqlalchemy
from sqlalchemy import select

from app.db.repositories.base import BaseRepository
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.hospital import HospitalRepository
from app.db.repositories.review import ReviewRepository
from app.db.tables.clients import clients
from app.db.tables.doctors import doctors
from app.db.tables.favorite_doctor import favorite_doctors
from app.db.tables.favorite_hospital import favorite_hospitals
from app.db.tables.hospitals import hospitals
from app.db.tables.reviews import reviews
from app.db.tables.visits import visits
from app.models.client import ClientOut, ClientIn
from app.models.doctor import DoctorOut
from app.models.hospital import HospitalOut


class ClientRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return clients

    @property
    def _schema_out(self) -> Type[ClientOut]:
        return ClientOut

    @property
    def _schema_in(self) -> Type[ClientIn]:
        return ClientIn

    async def get_by_credentials(self, email: str, password_hash: str):
        query = select(self.table)
        query = query.where(self.table.c.email == email,
                            self.table.c.password_hash == password_hash)
        client = await self._db.fetch_one(query)

        return ClientOut.parse_obj(client) if client else client

    async def get_favorite_hospitals(
            self,
            client_id: int,
            hospitals_repo: HospitalRepository,
    ) -> list[HospitalOut]:
        rows = await hospitals_repo._db.fetch_all(hospitals.select()
        .join(favorite_hospitals,
              hospitals.c.id == favorite_hospitals.c.hospital_id,
              isouter=True)
        .where(favorite_hospitals.c.hospital_id == client_id)
        .with_only_columns(
            hospitals.c.id,
            hospitals.c.name,
            hospitals.c.description,
            hospitals.c.photos,
            hospitals.c.phone,
            hospitals.c.email,
            hospitals.c.approved,
            hospitals.c.rating
        )
        )
        return [hospitals_repo._schema_out(**dict(row)) for row in rows] if rows else rows

    async def get_favorite_doctors(self,
                                   client_id: int,
                                   doctors_repo: DoctorRepository,
                                   ) -> list[DoctorOut]:
        rows = await doctors_repo._db.fetch_all(
            doctors.select()
            .join(favorite_doctors,
                  doctors.c.id == favorite_doctors.c.doctor_id,
                  isouter=True)
            .where(favorite_doctors.c.client_id == client_id)
            .with_only_columns(
                doctors.c.id,
                doctors.c.name,
                doctors.c.surname,
                doctors.c.patronomic,
                doctors.c.photo,
                doctors.c.email,
                doctors.c.rating,
                doctors.c.education,
                doctors.c.treatment_profile,
                doctors.c.work_experience,
                doctors.c.approved
            ))
        return [DoctorOut(**dict(row)) for row in rows] if rows else rows

    async def get_reviews(self,
                          client_id: int,
                          review_repo: ReviewRepository,
                          ):
        rows = await review_repo._db.fetch_all(review_repo.table.select()
        .join(visits, reviews.c.visit_id == visits.c.id, isouter=True)
        .join(doctors, reviews.c.doctor_id == doctors.c.id, isouter=True)
        .join(hospitals, reviews.c.hospital_id == hospitals.c.id, isouter=True)
        .where(visits.c.client_id == client_id)
        .with_only_columns(
            self.table.c.name.label('client_name'),
            self.table.c.surname.label('client_surname'),
            hospitals.c.name.label('hospital_name'),
            doctors.c.name.label('doctor_name'),
            visits.c.date_of_receipt,
            reviews.c.id,
            reviews.c.liked,
            reviews.c.did_not_liked,
            reviews.c.comment,
            reviews.c.review_time,
            reviews.c.confirmed,
        ))
        return [review_repo._schema_out(**dict(row)) for row in rows] if rows else rows
