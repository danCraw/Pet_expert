from datetime import datetime
from typing import Optional

from app.models.base import BaseSchema


class WorkDayBase(BaseSchema):
    service_id: int
    start_time: datetime
    end_time: datetime
    time_range: datetime


class WorkDayIn(WorkDayBase):
    work_day_id: Optional[int]


class WorkDayOut(WorkDayBase):
    work_day_id: int

