from sqlalchemy import Column, String, Table, Integer, Time

from app.db.base import metadata

Work_day = Table(
                'work_day',
                metadata,
                Column("id", Integer, primary_key=True),
                Column("service_id", String(65), nullable=False),
                Column("start_time", Time, nullable=False),
                Column("end_time", Time, nullable=False),
                Column("time_range", Integer, nullable=False)
                )
