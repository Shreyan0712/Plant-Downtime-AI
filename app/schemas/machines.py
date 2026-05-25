from pydantic import BaseModel
from typing import Optional
import datetime

class MachineCreate(BaseModel):

    machine_name: str

    location: Optional[str] = None

    category: Optional[str] = None

    install_date: Optional[datetime.date] = None

    status: Optional[str] = None

class MachineUpdate(BaseModel):

    machine_name: Optional[str] = None

    location: Optional[str] = None

    category: Optional[str] = None

    install_date: Optional[datetime.date] = None

    status: Optional[str] = None