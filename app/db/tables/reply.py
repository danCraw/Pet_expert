from sqlalchemy import Column, Table, Integer, ForeignKey, String, DateTime

from app.db.base import metadata

Reply = Table(
            'replies',
            metadata,
            Column("id", Integer, primary_key=True),
            Column("review_id", Integer, ForeignKey('review.id'), nullable=False),
            Column("client_id", Integer, ForeignKey('client.id'), nullable=False),
            Column("doctor_id", Integer, ForeignKey('doctor.id'), nullable=False),
            Column("hospital_id", Integer, ForeignKey('hospital.id'), nullable=False),
            Column("comment", String(2000), nullable=False),
            Column("reply_time", DateTime, nullable=False),
            )
