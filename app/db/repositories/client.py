from typing import Type

import sqlalchemy
from app.db.tables.clients import Client

from app.db.repositories.base import BaseRepository
from app.models.client import ClientOut, ClientIn
from app.models.doctor import DoctorOut
from app.models.hospital import HospitalOut


class ClientRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _table(self) -> sqlalchemy.Table:
        return Client

    @property
    def _schema_out(self) -> Type[ClientOut]:
        return ClientOut

    @property
    def _schema_in(self) -> Type[ClientIn]:
        return ClientIn

    async def get_favorite_hospitals(self, client_id: int, hospitals_repo, favourite_hospitals_table: sqlalchemy.Table) -> list[HospitalOut]:
        rows = await self._db.fetch_all(self._table.select()
        .join(favourite_hospitals_table,
              self._table.c.id == favourite_hospitals_table.c.client_id,
              isouter=True)
        .join(hospitals_repo,
              favourite_hospitals_table.c.hospital_id == hospitals_repo._table.c.id,
              isouter=True)
        .where(self._table.c.client_id == client_id)
        .with_only_columns(
            hospitals_repo._table.c.doctor_id,
            hospitals_repo._table.c.name,
            hospitals_repo._table.c.surname,
            hospitals_repo._table.c.patronomic,
            hospitals_repo._table.c.photo,
            hospitals_repo._table.c.email,
            hospitals_repo._table.c.rating,
            hospitals_repo._table.c.work_experience))
        return [hospitals_repo._schema_out(**dict(dict(row).items())) for row in rows] if rows else rows

    async def get_favorite_doctors(self, client_id: int, doctors_repo, favourite_doctors_table: sqlalchemy.Table) -> list[DoctorOut]:
        rows = await self._db.fetch_all(self._table.select()
        .join(favourite_doctors_table,
              self._table.c.id == favourite_doctors_table.c.client_id,
              isouter=True)
        .join(doctors_repo,
              favourite_doctors_table.c.doctor_id == doctors_repo._table.c.id,
              isouter=True)
        .where(self._table.c.client_id == client_id)
        .with_only_columns(
            doctors_repo._table.c.doctor_id,
            doctors_repo._table.c.name,
            doctors_repo._table.c.surname,
            doctors_repo._table.c.patronomic,
            doctors_repo._table.c.photo,
            doctors_repo._table.c.email,
            doctors_repo._table.c.rating,
            doctors_repo._table.c.work_experience))
        return [doctors_repo._schema_out(**dict(dict(row).items())) for row in rows] if rows else rows
