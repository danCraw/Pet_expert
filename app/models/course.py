from datetime import datetime
from typing import Optional

from app.models.base import BaseSchema


class CourseBase(BaseSchema):
    name: str
    description: str
    flaws: str
    photos: list[str]
    doctor_id: int


class CourseIn(CourseBase):
    course_id: Optional[int]


class CourseOut(CourseBase):
    course_id: int

