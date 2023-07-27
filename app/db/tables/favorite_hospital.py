from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata

FavoriteHospitals = Table(
                'favorite_hospitals',
                metadata,
                Column("client_id", Integer, ForeignKey('clients.client_id'), nullable=False),
                Column("hospital_id", Integer, ForeignKey('hospitals.hospital_id'), nullable=False)
)
