from typing import Optional
from datetime import datetime
from app.models.base import BaseSchema


class ReviewBase(BaseSchema):
    visit_id: int
    hospital_id: int
    doctor_id: int
    client_id: int
    liked: str
    did_not_liked: str
    comment: str
    review_time: datetime
    confirmed: bool


class ReviewIn(ReviewBase):
    review_id: Optional[int]


class ReviewOut(ReviewBase):
    review_id: int

