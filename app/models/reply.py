from app.models.base import BaseSchema


class ReplyBase(BaseSchema):
    review_id: int
    reply_review_id: int
