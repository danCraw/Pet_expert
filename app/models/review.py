from typing import Optional

from app.models.base import BaseSchema


class ReviewBase(BaseSchema):
    client_name: str
    visit_id: int
    confirmed: bool
    hospital_id: int
    doctor_id: int
    client_id: int


class ReviewIn(ReviewBase):
    review_id: Optional[int]


class ReviewOut(ReviewBase):
    review_id: int

