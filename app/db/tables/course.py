from sqlalchemy import Column, Table, Integer, ForeignKey, String, ARRAY

from app.db.base import metadata
from app.db.tables.doctors import Doctor

Course = Table(
                'courses',
                metadata,
                Column("id", Integer, primary_key=True),
                Column("name", Integer, nullable=False),
                Column("description", String(150), nullable=False),
                Column("photos", ARRAY(String(150)), nullable=False),
                Column("doctor_id", Integer, nullable=False),
                Column("doctor_id", Integer, ForeignKey(Doctor.doctor_id), nullable=False)
)
