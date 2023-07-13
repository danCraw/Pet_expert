from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata
from app.db.tables.reviews import Review

Response = Table(
                'response',
                metadata,
                Column("review_id", Integer, primary_key=True),
                Column("response_review_id", Integer, nullable=False),
                Column("review_id", Integer, ForeignKey(Review.review_id), nullable=False),
                Column("response_review_id", Integer, ForeignKey(Review.review_id), nullable=False)
                )
