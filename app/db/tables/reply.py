from sqlalchemy import Column, Table, Integer, ForeignKey

from app.db.base import metadata

Reply = Table(
            'reply',
            metadata,
            Column("reply_id", Integer, ForeignKey('review.id'), nullable=False),
            Column("reply_review_id", Integer, ForeignKey('review.id'), nullable=False)
            )
