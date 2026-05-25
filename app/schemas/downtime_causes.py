from pydantic import BaseModel
from typing import Optional


class DowntimeCauseCreate(BaseModel):

    downtime_id: int

    root_cause: Optional[str] = None

    category: Optional[str] = None

    corrective_action: Optional[str] = None

    preventive_action: Optional[str] = None


class DowntimeCauseUpdate(BaseModel):

    downtime_id: int

    root_cause: Optional[str] = None

    category: Optional[str] = None

    corrective_action: Optional[str] = None

    preventive_action: Optional[str] = None