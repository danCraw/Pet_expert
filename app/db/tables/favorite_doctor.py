from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata

favorite_doctors = Table(
                'favorite_doctors',
                metadata,
                Column("client_id", Integer, ForeignKey("clients.id"), nullable=False),
                Column("doctor_id", Integer, ForeignKey("doctors.id"), nullable=False),
)
