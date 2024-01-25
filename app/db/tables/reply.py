from sqlalchemy import Column, Table, Integer, ForeignKey, String, DateTime

from app.db.base import metadata

Reply = Table(
            'replies',
            metadata,
            Column("id", Integer, primary_key=True),
            Column("review_id", Integer, ForeignKey('review.id'), nullable=False),
            Column("comment", String(2000), nullable=False),
            Column("review_time", DateTime, nullable=False),
            )
