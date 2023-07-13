from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata
from app.db.tables.clients import Client
from app.db.tables.doctors import Doctor

Doctor_hospital = Table(
                'doctor_hospital',
                metadata,
                Column("client_id", Integer, primary_key=True),
                Column("doctor_id", Integer, nullable=False),
                Column("client_id", Integer, ForeignKey(Client.service_id), nullable=False),
                Column("doctor_id", Integer, ForeignKey(Doctor.service_id), nullable=False)
)
