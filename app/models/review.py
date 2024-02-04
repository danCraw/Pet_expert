from typing import Optional
from datetime import datetime, date
from app.models.base import BaseSchema


class ReviewBase(BaseSchema):
    visit_id: int
    hospital_id: int
    doctor_id: int
    doctor_assessment: int | None = 0
    hospital_assessment: int | None = 0
    liked: str
    did_not_liked: str
    comment: str
    review_time: datetime
    confirmed: bool


class ReviewIn(ReviewBase):
    id: Optional[int]


class ReviewOut(ReviewBase):
    id: int | None
    visit_id: int | None
    hospital_id: int | None
    doctor_id: int | None
    client_name: str
    client_surname: str
    liked: str
    did_not_liked: str
    comment: str
    review_time: datetime
    confirmed: str
    date_of_receipt: date | None
    hospital_name: str | None
    doctor_name: str | None
