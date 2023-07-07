from sqlalchemy import Column, String, Table, Integer

from app.db.base import metadata

Day_of_week = Table(
                'day_of_week',
                metadata,
                Column("day_of_week_id", Integer, primary_key=True),
                Column("day_of_week_name", String(65), nullable=False)
                )
