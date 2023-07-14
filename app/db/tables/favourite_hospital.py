from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata
from app.db.tables.clients import Client
from app.db.tables.hospitals import Hospital

Favourite_hospitals = Table(
                'favourite_hospitals',
                metadata,
                Column("client_id", Integer, primary_key=True),
                Column("hospital_id", Integer, nullable=False),
                Column("client_id", Integer, ForeignKey(Client.service_id), nullable=False),
                Column("hospital_id", Integer, ForeignKey(Hospital.service_id), nullable=False)
)
