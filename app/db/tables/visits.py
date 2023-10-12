from sqlalchemy import Column, String, Table, Integer, ARRAY, Date, ForeignKey

from app.db.base import metadata

Visit = Table(
    'visits',
    metadata,
    Column("id", Integer, primary_key=True, nullable=True),
    Column("client_id", Integer, ForeignKey('clients.id'), nullable=False),
    Column("diagnosis", String(65), nullable=False),
    Column("photos", ARRAY(String(65)), nullable=False),
    Column("date_of_receipt", Date, nullable=False),
    Column("pet_name", String(65), nullable=False),
    Column("pet_age", String(65), nullable=False),
    Column("pet_breed", String(65), nullable=False),
    Column("pet_type", String(65), nullable=False)
)
