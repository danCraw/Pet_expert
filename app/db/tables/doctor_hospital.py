from sqlalchemy import Column, Table, Integer, ForeignKey, DATE

from app.db.base import metadata
from app.db.tables.hospitals import hospitals
from app.db.tables.doctors import doctors

doctor_hospital = Table(
                'doctor_hospital',
                metadata,
                Column("start_date", DATE, nullable=False),
                Column("end_date", DATE, nullable=True),
                Column("hospital_id", Integer, ForeignKey(hospitals.c.id), nullable=False),
                Column("doctor_id", Integer, ForeignKey(doctors.c.id), nullable=False)
)
