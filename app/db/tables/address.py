from sqlalchemy import Column, String, Table, Integer, ForeignKey

from app.db.base import metadata
from app.db.tables.hospitals import hospitals

address = Table(
                'addresses',
                metadata,
                Column("id", Integer, primary_key=True),
                Column("hospital_id", Integer, ForeignKey(hospitals.hospital_id), nullable=False),
                Column("city", String(65), nullable=False),
                Column("street", String(65), nullable=False),
                Column("number", Integer, nullable=False)
                )
