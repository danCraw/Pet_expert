from sqlalchemy import Column, String, Table, Integer, ARRAY, DATE

from app.db.base import metadata

Visit = Table(
                'visits',
                metadata,
                Column("visit_id", Integer, primary_key=True),
                Column("diagnosis", String(65), nullable=False),
                Column("dignity", String(1000), nullable=False),
                Column("flaws", String(1000), nullable=False),
                Column("photos", ARRAY[String(65)], nullable=False),
                Column("date_of_receipt", DATE, nullable=False),
                Column("phone", String(65), nullable=False),
                Column("pet_name", String(65), nullable=False),
                Column("pet_age", String(65), nullable=False),
                Column("pet_breed", String(65), nullable=False),
                Column("pet_typet", String(65), nullable=False),
                )
