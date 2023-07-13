from datetime import datetime
from typing import Optional

from app.models.base import BaseSchema


class DayOfWeekBase(BaseSchema):
    day_of_week_name: str


class DayOfWeekIn(DayOfWeekBase):
    day_of_week_id: Optional[int]


class DayOfWeekOut(DayOfWeekBase):
    day_of_week_id: int

