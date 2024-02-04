from sqlalchemy import Column, String, Table, Integer, Boolean, ForeignKey, DateTime

from app.db.base import metadata

reviews = Table(
                'reviews',
                metadata,
                Column("id", Integer, primary_key=True),
                Column("visit_id", Integer, ForeignKey('visits.id'), nullable=False),
                Column("hospital_id", Integer, ForeignKey('hospitals.id'), nullable=False),
                Column("doctor_id", Integer, ForeignKey('doctors.id'), nullable=False),
                Column("doctor_assessment", Integer, default=0, nullable=False),
                Column("hospital_assessment", Integer, default=0, nullable=False),
                Column("liked", String(2000), nullable=False),
                Column("did_not_liked", String(2000), nullable=False),
                Column("comment", String(2000), nullable=False),
                Column("review_time", DateTime, nullable=False),
                Column("confirmed", Boolean, nullable=False)
                )
