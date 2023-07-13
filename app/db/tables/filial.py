from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata
from app.db.tables.hospitals import Hospital

Filial = Table(
                'filial',
                metadata,
                Column("hospital_id", Integer, ForeignKey(Hospital.review_id), primary_key=True),
                Column("filial_id", Integer, ForeignKey(Hospital.review_id), nullable=False),
                Column("hospital_id", Integer, ForeignKey(Hospital.hospital_id), nullable=False),
                Column("filial_id", Integer, ForeignKey(Hospital.hospital_id), nullable=False)
                )
