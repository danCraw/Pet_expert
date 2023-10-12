from sqlalchemy import Column, String, Table, Integer, Time, ForeignKey

from app.db.base import metadata
from app.db.tables.services import Service
from app.db.tables.doctors import Doctor

Doctor_service = Table(
                'doctor_service',
                metadata,
                Column("doctor_id", Integer, primary_key=True),
                Column("service_id", Integer, nullable=False),
                Column("price", Integer, nullable=False),
                Column("service_id", Integer, ForeignKey(Service.id), nullable=False),
                Column("doctor_id", Integer, ForeignKey(Doctor.id), nullable=False)
)
