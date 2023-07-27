from sqlalchemy import Column, String, Table, Integer, Boolean, ForeignKey, DateTime

from app.db.base import metadata

Review = Table(
                'reviews',
                metadata,
                Column("review_id", Integer, primary_key=True),
                Column("visit_id", Integer, ForeignKey('visits.visit_id'), nullable=False),
                Column("hospital_id", Integer, ForeignKey('hospitals.hospital_id'), nullable=False),
                Column("doctor_id", Integer, ForeignKey('doctors.doctor_id'), nullable=False),
                Column("liked", String(2000), nullable=False),
                Column("did_not_liked", String(2000), nullable=False),
                Column("comment", String(2000), nullable=False),
                Column("review_time", DateTime, nullable=False),
                Column("confirmed", Boolean, nullable=False)
                )
