from pydantic import BaseModel, field_validator
from typing import Optional


class DowntimeCauseCreate(BaseModel):

    downtime_id: int

    root_cause: Optional[str] = None

    category: Optional[str] = None

    corrective_action: Optional[str] = None

    preventive_action: Optional[str] = None

    @field_validator("category")
    @classmethod
    def normalize_category(cls, v):
        if v is None:
            return v
        return v.strip().capitalize()


class DowntimeCauseUpdate(BaseModel):

    downtime_id: int

    root_cause: Optional[str] = None

    category: Optional[str] = None

    corrective_action: Optional[str] = None

    preventive_action: Optional[str] = None

    @field_validator("category")
    @classmethod
    def normalize_category(cls, v):
        if v is None:
            return v
        return v.strip().capitalize()