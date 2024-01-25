from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata
from app.db.tables.day_of_week import Day_of_week
from app.db.tables.doctors import doctors
from app.db.tables.work_day import Work_day

Course = Table(
                'schedule',
                metadata,
                Column("id", Integer, primary_key=True),
                Column("doctor_id", Integer, nullable=False),
                Column("day_of_week_id", Integer, nullable=False),
                Column("work_day_id", Integer, nullable=False),
                Column("doctor_id", Integer, nullable=False),
                Column("doctor_id", Integer, ForeignKey(doctors.id), nullable=False),
                Column("day_of_week_id", Integer, ForeignKey(Day_of_week.id), nullable=False),
                Column("work_day_id", Integer, ForeignKey(Work_day.id), nullable=False)
)
