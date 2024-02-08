from sqlalchemy import Column, Table, Integer, ForeignKey, DATE

from app.db.base import metadata
from app.db.tables.hospitals import hospitals
from app.db.tables.doctors import doctors

Doctor_hospital = Table(
                'doctor_hospital',
                metadata,
                Column("doctor_id", Integer, primary_key=True),
                Column("service_id", Integer, nullable=False),
                Column("start_date", DATE, nullable=False),
                Column("end_date", DATE, nullable=True),
                Column("service_id", Integer, ForeignKey(hospitals.id), nullable=False),
                Column("doctor_id", Integer, ForeignKey(doctors.id), nullable=False)
)
