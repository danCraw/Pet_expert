from datetime import datetime

from app.models.base import BaseSchema


class ReplyBase(BaseSchema):
    id: int
    review_id: int
    client_id: int | None
    doctor_id: int | None
    hospital_id: int | None
    comment: str
    reply_time: datetime


class ReplyIn(ReplyBase):
    id: int | None


class ReplyOut(ReplyBase):
    id: int | None
