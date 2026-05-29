from pydantic import BaseModel, field_validator
from typing import Optional
import datetime


class MachineCreate(BaseModel):

    machine_name: str

    location: Optional[str] = None

    category: Optional[str] = None

    install_date: Optional[datetime.date] = None

    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def normalize_status(cls, v):
        if v is None:
            return v
        return v.strip().capitalize()

class MachineUpdate(BaseModel):

    machine_name: Optional[str] = None

    location: Optional[str] = None

    category: Optional[str] = None

    install_date: Optional[datetime.date] = None

    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def normalize_status(cls, v):
        if v is None:
            return v
        return v.strip().capitalize()
