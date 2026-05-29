from pydantic import BaseModel, field_validator
from typing import Optional
import datetime

class MaintenanceLogCreate(BaseModel):

    machine_id: int

    maintenance_type: Optional[str] = None

    start_time: Optional[datetime.datetime] = None

    end_time: Optional[datetime.datetime] = None

    work_done: Optional[str] = None

    technician: Optional[str] = None

    @field_validator("maintenance_type")
    @classmethod
    def normalize_maintenance_type(cls, v):
        if v is None:
            return v
        return v.strip().capitalize()

class MaintenanceLogUpdate(BaseModel):
    
    machine_id: int

    maintenance_type: Optional[str] = None

    start_time: Optional[datetime.datetime] = None

    end_time: Optional[datetime.datetime] = None

    work_done: Optional[str] = None

    technician: Optional[str] = None

    @field_validator("maintenance_type")
    @classmethod
    def normalize_maintenance_type(cls, v):
        if v is None:
            return v
        return v.strip().capitalize()