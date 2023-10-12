from sqlalchemy import Column, String, Table, Integer, Time, ForeignKey, DATE

from app.db.base import metadata
from app.db.tables.hospitals import Hospital
from app.db.tables.doctors import Doctor

Doctor_hospital = Table(
                'doctor_hospital',
                metadata,
                Column("doctor_id", Integer, primary_key=True),
                Column("service_id", Integer, nullable=False),
                Column("start_date", DATE, nullable=False),
                Column("end_date", DATE, nullable=True),
                Column("service_id", Integer, ForeignKey(Hospital.id), nullable=False),
                Column("doctor_id", Integer, ForeignKey(Doctor.id), nullable=False)
)
