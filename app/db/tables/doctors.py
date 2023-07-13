from sqlalchemy import Column, String, Table, Integer, Float

from app.db.base import metadata

Doctor = Table(
                'doctors',
                metadata,
                Column("doctor_id", Integer, primary_key=True),
                Column("name", String(65), nullable=False),
                Column("surname", String(65), nullable=False),
                Column("patronomic", String(65), nullable=False),
                Column("photo", String(65), nullable=False),
                Column("email", String(65), nullable=False),
                Column("password_hash", String(65), nullable=False),
                Column("rating", Float, nullable=False),
                Column("education", String(150), nullable=False),
                Column("treatment_profile", String(1000), nullable=False),
                Column("work_experience", Integer, nullable=False)
)
