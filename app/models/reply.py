from datetime import datetime

from app.models.base import BaseSchema


class ReplyBase(BaseSchema):
    review_id: int
    comment: str
    review_time: datetime


class ReplyIn(ReplyBase):
    id: int | None


class ReplyOut(ReplyBase):
    id: int | None
