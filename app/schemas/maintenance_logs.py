from pydantic import BaseModel
from typing import Optional
import datetime

class MaintenanceLogCreate(BaseModel):

    machine_id: int

    maintenance_type: Optional[str] = None

    start_time: Optional[datetime.datetime] = None

    end_time: Optional[datetime.datetime] = None

    work_done: Optional[str] = None

    technician: Optional[str] = None

class MaintenanceLogUpdate(BaseModel):
    
    machine_id: int

    maintenance_type: Optional[str] = None

    start_time: Optional[datetime.datetime] = None

    end_time: Optional[datetime.datetime] = None

    work_done: Optional[str] = None

    technician: Optional[str] = None