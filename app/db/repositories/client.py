from typing import Type

import sqlalchemy

from app.db.repositories.base import BaseRepository
from app.db.repositories.doctor import DoctorRepository
from app.db.repositories.favorite_doctor import FavoriteDoctorsRepository
from app.db.repositories.favourite_hospital import FavoriteHospitalsRepository
from app.db.repositories.hospital import HospitalRepository
from app.db.repositories.review import ReviewRepository
from app.db.tables.clients import Client
from app.db.tables.doctors import Doctor
from app.db.tables.favorite_doctor import FavoriteDoctors
from app.db.tables.favorite_hospital import FavoriteHospitals
from app.db.tables.hospitals import Hospital
from app.db.tables.visits import Visit
from app.models.client import ClientOut, ClientIn
from app.models.doctor import DoctorOut
from app.models.favorite_doctor import FavouriteDoctor
from app.models.favorite_hospital import FavouriteHospital
from app.models.hospital import HospitalOut


class ClientRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def table(self) -> sqlalchemy.Table:
        return Client

    @property
    def _schema_out(self) -> Type[ClientOut]:
        return ClientOut

    @property
    def _schema_in(self) -> Type[ClientIn]:
        return ClientIn

    async def add_hospital_to_favorite(self,
                                       favourite_hospital: FavouriteHospital,
                                       favourite_hospitals_repo: FavoriteHospitalsRepository):
        favourite_hospital = await favourite_hospitals_repo.create(favourite_hospital)
        return favourite_hospital

    async def get_favorite_hospitals(self,
                                     client_id: int,
                                     hospitals_repo: HospitalRepository,
                                     favourite_hospitals_table: FavoriteHospitals
                                     ) -> list[HospitalOut]:
        rows = await hospitals_repo._db.fetch_all(hospitals_repo.table.select()
                                                  .join(favourite_hospitals_table,
                                                        hospitals_repo.table.c.id == favourite_hospitals_table.c.hospital_id,
                                                        isouter=True)
                                                  .where(favourite_hospitals_table.c.hospital_id == client_id)
                                                  .with_only_columns(
                                                        hospitals_repo.table.c.id,
                                                        hospitals_repo.table.c.name,
                                                        hospitals_repo.table.c.description,
                                                        hospitals_repo.table.c.photos,
                                                        hospitals_repo.table.c.phone,
                                                        hospitals_repo.table.c.email,
                                                        hospitals_repo.table.c.approved
        )
                                                  )
        return [hospitals_repo._schema_out(**dict(dict(row).items())) for row in rows] if rows else rows

    async def add_doctor_to_favorite(self,
                                     favourite_doctor: FavouriteDoctor,
                                     favourite_doctors_repo: FavoriteDoctorsRepository):
        favourite_doctor = await favourite_doctors_repo.create(favourite_doctor)
        return favourite_doctor

    async def get_favorite_doctors(self,
                                   client_id: int,
                                   doctors_repo: DoctorRepository,
                                   favourite_doctors_table: FavoriteDoctors
                                   ) -> list[DoctorOut]:
        rows = await doctors_repo._db.fetch_all(doctors_repo.table.select()
        .join(favourite_doctors_table,
              doctors_repo.table.c.id == favourite_doctors_table.c.doctor_id,
              isouter=True)
        .where(favourite_doctors_table.c.client_id == client_id)
        .with_only_columns(
              doctors_repo.table.c.id,
              doctors_repo.table.c.name,
              doctors_repo.table.c.surname,
              doctors_repo.table.c.patronomic,
              doctors_repo.table.c.photo,
              doctors_repo.table.c.email,
              doctors_repo.table.c.rating,
              doctors_repo.table.c.education,
              doctors_repo.table.c.treatment_profile,
              doctors_repo.table.c.work_experience,
              doctors_repo.table.c.approved
        ))
        return [doctors_repo._schema_out(**dict(dict(row).items())) for row in rows] if rows else rows

    async def get_reviews(self,
                          client_id: int,
                          review_repo: ReviewRepository,
                          visits_table: Visit,
                          doctors_table: Doctor,
                          hospitals_table: Hospital,
                          ):
        rows = await review_repo._db.fetch_all(review_repo.table.select()
        .join(visits_table, review_repo.table.c.visit_id == visits_table.c.id, isouter=True)
        .join(doctors_table, review_repo.table.c.doctor_id == doctors_table.c.id, isouter=True)
        .join(hospitals_table, review_repo.table.c.hospital_id == hospitals_table.c.id, isouter=True)
        .where(visits_table.c.client_id == client_id)
        .with_only_columns(
         hospitals_table.c.name.label('hospital_name'),
         doctors_table.c.name.label('doctor_name'),
         visits_table.c.date_of_receipt,
         review_repo.table.c.liked,
         review_repo.table.c.did_not_liked,
         review_repo.table.c.comment,
         review_repo.table.c.review_time,
         review_repo.table.c.confirmed,
        ))
        return [review_repo._schema_out(**dict(row)) for row in rows] if rows else rows
