from sqlalchemy import Column, String, Table, Integer

from app.db.base import metadata

Hospital = Table(
                'hospitals',
                metadata,
                Column("hospital_id", Integer, primary_key=True),
                Column("name", String(65), nullable=False),
                Column("description", String(65), nullable=False),
                Column("photo", String(65), nullable=False),
                Column("email", String(65), nullable=False),
                Column("password_hash", String(65), nullable=False)
                )
