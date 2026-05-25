from pydantic import BaseModel
from typing import Optional
import datetime


class DowntimeEventCreate(BaseModel):

    machine_id: int

    start_time: datetime.datetime

    end_time: Optional[datetime.datetime] = None

    downtime_minutes: Optional[int] = None

    reason_category: Optional[str] = None

    reason_details: Optional[str] = None

    reported_by: Optional[str] = None


class DowntimeEventUpdate(BaseModel):

    machine_id: int

    start_time: datetime.datetime

    end_time: Optional[datetime.datetime] = None

    downtime_minutes: Optional[int] = None

    reason_category: Optional[str] = None

    reason_details: Optional[str] = None

    reported_by: Optional[str] = None