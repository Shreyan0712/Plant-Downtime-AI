from sqlalchemy.orm import Session

from app.models.models import DowntimeCauses

from app.schemas.downtime_causes import (
    DowntimeCauseCreate,
    DowntimeCauseUpdate
)


# Get all causes
def get_all_downtime_causes(
    db: Session
):

    return db.query(DowntimeCauses).all()


# Get cause by ID
def get_downtime_cause_by_id(
    db: Session,
    cause_id: int
):

    return db.query(DowntimeCauses).filter(
        DowntimeCauses.cause_id == cause_id
    ).first()


# Add cause
def create_downtime_cause(
    db: Session,
    cause: DowntimeCauseCreate
):

    db_cause = DowntimeCauses(
        downtime_id=cause.downtime_id,
        root_cause=cause.root_cause,
        category=cause.category,
        corrective_action=cause.corrective_action,
        preventive_action=cause.preventive_action
    )

    db.add(db_cause)

    db.commit()

    db.refresh(db_cause)

    return db_cause


# Delete cause
def delete_downtime_cause(
    db: Session,
    cause_id: int
):

    cause = db.query(DowntimeCauses).filter(
        DowntimeCauses.cause_id == cause_id
    ).first()

    if cause:

        db.delete(cause)

        db.commit()

    return cause


# Update cause
def update_downtime_cause(
    db: Session,
    cause_id: int,
    updated_cause: DowntimeCauseUpdate
):

    cause = db.query(DowntimeCauses).filter(
        DowntimeCauses.cause_id == cause_id
    ).first()

    if cause:

        cause.downtime_id = updated_cause.downtime_id
        cause.root_cause = updated_cause.root_cause
        cause.category = updated_cause.category
        cause.corrective_action = updated_cause.corrective_action
        cause.preventive_action = updated_cause.preventive_action

        db.commit()

        db.refresh(cause)

    return cause