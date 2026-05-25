from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.maintenance_logs import (
    MaintenanceLogCreate,
    MaintenanceLogUpdate
)
from app.crud.maintenance_logs import (
    get_all_maintenance_logs,
    get_maintenance_logs_by_id,
    add_maintenance_log,
    delete_maintenance_log,
    update_log
)

router = APIRouter()

#Get all Logs
@router.get("/maintenance-logs")
def fetch_maintenance_logs(
    db:Session = Depends(get_db)
):
    return get_all_maintenance_logs(db)

#Get log by id
@router.get("/maintenance-logs/{maintenance_id}")
def fetch_maintenance_logs_by_id(
    maintenance_id: int,
    db:Session = Depends(get_db)
):
    
    return get_maintenance_logs_by_id(
        db,
        maintenance_id
    )

#Add maintenance log
@router.post("/maintenance-logs")
def create_maintenance_log(
    maintenance_log: MaintenanceLogCreate,
    db: Session = Depends(get_db)
):
    
    return add_maintenance_log(
        maintenance_log,
        db
    )

#Delete log
@router.delete("/maintenance-logs/{maintenance_id}")
def delete_maintenance_log_by_id(
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    return delete_maintenance_log(
        db,
        maintenance_id
    )

#Update Log
@router.put("/maintenance-logs/{maintenance_id}")
def update_maintenance_log(
    new_log: MaintenanceLogUpdate,
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    return update_log(
        new_log,
        maintenance_id,
        db
    )