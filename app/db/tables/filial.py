from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata
from app.db.tables.hospitals import hospitals

Filial = Table(
                'filial',
                metadata,
                Column("hospital_id", Integer, ForeignKey(hospitals.id), primary_key=True),
                Column("filial_id", Integer, ForeignKey(hospitals.id), nullable=False)
                )
