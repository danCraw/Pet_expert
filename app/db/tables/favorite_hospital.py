from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata

favorite_hospitals = Table(
                'favorite_hospitals',
                metadata,
                Column("client_id", Integer, ForeignKey('clients.id'), nullable=False),
                Column("hospital_id", Integer, ForeignKey('hospitals.id'), nullable=False)
)
