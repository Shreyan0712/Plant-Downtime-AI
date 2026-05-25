from sqlalchemy.orm import Session
from app.models.models import MaintenanceLogs

from app.schemas.maintenance_logs import (
    MaintenanceLogCreate,
    MaintenanceLogUpdate
)

#Get all maintenancce logs
def get_all_maintenance_logs(db:Session):

    return db.query(MaintenanceLogs).all()

#Get maintenance logs by maintenance_id
def get_maintenance_logs_by_id(
    db: Session,
    maintenance_id: int
):
    return db.query(MaintenanceLogs).filter(
        MaintenanceLogs.maintenance_id == maintenance_id
    ).first()

# Add maintenance log
def add_maintenance_log(
    maintenance_log: MaintenanceLogCreate,
    db: Session
):

    db_log = MaintenanceLogs(
        machine_id=maintenance_log.machine_id,
        maintenance_type=maintenance_log.maintenance_type,
        start_time=maintenance_log.start_time,
        end_time=maintenance_log.end_time,
        work_done=maintenance_log.work_done,
        technician=maintenance_log.technician
    )

    db.add(db_log)

    db.commit()

    db.refresh(db_log)

    return db_log


#Delete maintenance log by maintenace_id
def delete_maintenance_log(
    db: Session,
    maintenance_id:int
):
    maintenance_log = db.query(MaintenanceLogs).filter(
        MaintenanceLogs.maintenance_id == maintenance_id
    ).first()

    if maintenance_log:
        
        db.delete(maintenance_log)

        db.commit()
    
    return maintenance_log

#Maintenance Log update
def update_log(
    update_log: MaintenanceLogUpdate,
    maintenance_id: int,
    db: Session
):

    log = db.query(MaintenanceLogs).filter(
        MaintenanceLogs.maintenance_id == maintenance_id
    ).first()

    if log:
        log.machine_id = update_log.machine_id
        log.maintenance_type = update_log.maintenance_type
        log.start_time = update_log.start_time
        log.end_time = update_log.end_time
        log.work_done = update_log.work_done
        log.technician = update_log.technician

        db.commit()

        db.refresh(log)

    return log