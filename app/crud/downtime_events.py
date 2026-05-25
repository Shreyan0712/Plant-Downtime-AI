from sqlalchemy.orm import Session

from app.models.models import DowntimeEvents

from app.schemas.downtime_events import (
    DowntimeEventCreate,
    DowntimeEventUpdate
)

#Get all downtime events
def get_all_downtime_events(db: Session):

    return db.query(DowntimeEvents).all()

#Get downtime event by id
def get_downtime_event_by_id(
    db: Session,
    downtime_id: int
):

    return db.query(DowntimeEvents).filter(
        DowntimeEvents.downtime_id == downtime_id
    ).first()

#Create new downtime event 
def create_downtime_event(
    db: Session,
    event: DowntimeEventCreate
):

    db_event = DowntimeEvents(
        machine_id=event.machine_id,
        start_time=event.start_time,
        end_time=event.end_time,
        downtime_minutes=event.downtime_minutes,
        reason_category=event.reason_category,
        reason_details=event.reason_details,
        reported_by=event.reported_by
    )

    db.add(db_event)

    db.commit()

    db.refresh(db_event)

    return db_event

#Delete Downtime event
def delete_downtime_event(
    db: Session,
    downtime_id: int
):

    event = db.query(DowntimeEvents).filter(
        DowntimeEvents.downtime_id == downtime_id
    ).first()

    if event:

        db.delete(event)

        db.commit()

    return event

#Update downtime event
def update_downtime_event(
    db: Session,
    downtime_id: int,
    updated_event: DowntimeEventUpdate
):

    event = db.query(DowntimeEvents).filter(
        DowntimeEvents.downtime_id == downtime_id
    ).first()

    if event:

        event.machine_id = updated_event.machine_id
        event.start_time = updated_event.start_time
        event.end_time = updated_event.end_time
        event.downtime_minutes = updated_event.downtime_minutes
        event.reason_category = updated_event.reason_category
        event.reason_details = updated_event.reason_details
        event.reported_by = updated_event.reported_by

        db.commit()

        db.refresh(event)

    return event