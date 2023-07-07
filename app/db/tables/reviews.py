from sqlalchemy import Column, String, Table, Integer, Boolean, ForeignKey

from app.db.base import metadata
from app.db.tables.clients import Client
from app.db.tables.doctors import Doctor
from app.db.tables.hospitals import Hospital
from app.db.tables.visits import Visit

Review = Table(
                'reviews',
                metadata,
                Column("review_id", Integer, primary_key=True),
                Column("client_name", String(65), nullable=False),
                Column("visit_id", Integer, ForeignKey(Visit.visit_id), nullable=False),
                Column("confirmed", Boolean, nullable=False),
                Column("hospital_id", Integer, ForeignKey(Hospital.hospital_id), nullable=False),
                Column("doctor_id", Integer, ForeignKey(Doctor.doctor_id), nullable=False),
                Column("client_id", Integer, ForeignKey(Client.client_id), nullable=False)
                )
