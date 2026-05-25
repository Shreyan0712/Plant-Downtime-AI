from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.downtime_events import (
    DowntimeEventCreate,
    DowntimeEventUpdate
)

from app.crud.downtime_events import (
    get_all_downtime_events,
    get_downtime_event_by_id,
    create_downtime_event,
    delete_downtime_event,
    update_downtime_event
)

router = APIRouter()

#Get all downtime events endpoint
@router.get("/downtime-events")
def fetch_all_downtime_events(
    db: Session = Depends(get_db)
):

    return get_all_downtime_events(db)

#Get dowtime event by id endpoint
@router.get("/downtime-events/{downtime_id}")
def fetch_downtime_event_by_id(
    downtime_id: int,
    db: Session = Depends(get_db)
):

    return get_downtime_event_by_id(
        db,
        downtime_id
    )

#Add downtime endpoint event
@router.post("/downtime-events")
def add_downtime_event(
    event: DowntimeEventCreate,
    db: Session = Depends(get_db)
):

    return create_downtime_event(
        db,
        event
    )

#Remove downtime event endpoint
@router.delete("/downtime-events/{downtime_id}")
def remove_downtime_event(
    downtime_id: int,
    db: Session = Depends(get_db)
):

    return delete_downtime_event(
        db,
        downtime_id
    )

#Edit dowtime event
@router.put("/downtime-events/{downtime_id}")
def edit_downtime_event(
    downtime_id: int,
    updated_event: DowntimeEventUpdate,
    db: Session = Depends(get_db)
):

    return update_downtime_event(
        db,
        downtime_id,
        updated_event
    )