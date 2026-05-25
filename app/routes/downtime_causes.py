from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.downtime_causes import (
    DowntimeCauseCreate,
    DowntimeCauseUpdate
)

from app.crud.downtime_causes import (
    get_all_downtime_causes,
    get_downtime_cause_by_id,
    create_downtime_cause,
    delete_downtime_cause,
    update_downtime_cause
)

router = APIRouter()


# Get all causes
@router.get("/downtime-causes")
def fetch_all_downtime_causes(
    db: Session = Depends(get_db)
):

    return get_all_downtime_causes(db)


# Get cause by ID
@router.get("/downtime-causes/{cause_id}")
def fetch_downtime_cause_by_id(
    cause_id: int,
    db: Session = Depends(get_db)
):

    return get_downtime_cause_by_id(
        db,
        cause_id
    )


# Add cause
@router.post("/downtime-causes")
def add_downtime_cause(
    cause: DowntimeCauseCreate,
    db: Session = Depends(get_db)
):

    return create_downtime_cause(
        db,
        cause
    )


# Delete cause
@router.delete("/downtime-causes/{cause_id}")
def remove_downtime_cause(
    cause_id: int,
    db: Session = Depends(get_db)
):

    return delete_downtime_cause(
        db,
        cause_id
    )


# Update cause
@router.put("/downtime-causes/{cause_id}")
def edit_downtime_cause(
    cause_id: int,
    updated_cause: DowntimeCauseUpdate,
    db: Session = Depends(get_db)
):

    return update_downtime_cause(
        db,
        cause_id,
        updated_cause
    )