from pydantic import BaseModel, field_validator
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

    @field_validator("reason_category")
    @classmethod
    def normalize_reason_category(cls, v):
        if v is None:
            return v
        return v.strip().capitalize()


class DowntimeEventUpdate(BaseModel):

    machine_id: int

    start_time: datetime.datetime

    end_time: Optional[datetime.datetime] = None

    downtime_minutes: Optional[int] = None

    reason_category: Optional[str] = None

    reason_details: Optional[str] = None

    reported_by: Optional[str] = None

    @field_validator("reason_category")
    @classmethod
    def normalize_reason_category(cls, v):
        if v is None:
            return v
        return v.strip().capitalize()