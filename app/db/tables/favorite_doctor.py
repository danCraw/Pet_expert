from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata

FavoriteDoctors = Table(
                'favorite_doctors',
                metadata,
                Column("client_id", Integer, ForeignKey("clients.client_id"), nullable=False),
                Column("doctor_id", Integer, ForeignKey("doctors.doctor_id"), nullable=False),
)
