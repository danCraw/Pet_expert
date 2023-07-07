from sqlalchemy import Column, String, Table, Integer

from app.db.base import metadata

Service = Table(
                'services',
                metadata,
                Column("service_id", Integer, primary_key=True),
                Column("name", String(65), nullable=False),
                Column("description", String(150), nullable=False)
                )
