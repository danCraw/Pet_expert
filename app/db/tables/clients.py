from sqlalchemy import Column, String, Table, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import metadata

Client = Table(
                'clients',
                metadata,
                Column("client_id", Integer, primary_key=True),
                Column("name", String(65), nullable=False),
                Column("surname", String(65), nullable=False),
                Column("patronomic", String(65), nullable=False),
                Column("photo", String(65), nullable=False),
                Column("phone", String(65), nullable=False),
                Column("email", String(65), nullable=False),
                Column("password_hash", String(65), nullable=False))
