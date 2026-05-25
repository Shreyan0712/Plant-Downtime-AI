from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.machines import (
    MachineCreate,
    MachineUpdate
)
from app.crud.machines import (
    get_all_machines,
    get_machine_by_id,
    create_machine,
    delete_machine,
    update_machine
)

router = APIRouter()

#Get all machine endpoint
@router.get("/machines")
def fetch_machines(
    db: Session = Depends(get_db)
):

    return get_all_machines(db)

#Machines by machine_id endpoint
@router.get("/machines/{machine_id}")
def fetch_by_machine_id(
    machine_id: int,
    db:Session = Depends(get_db)
    ):

    return get_machine_by_id(
        db,
        machine_id
    )

#Add machine endpoint
@router.post("/machines")
def add_machine(
    machine: MachineCreate,
    db: Session = Depends(get_db)
):
    return create_machine(
        db,
        machine
    )

#Delete machine by machine_id endpoint
@router.delete("/machines/{machine_id}")
def remove_machine(
    machine_id: int,
    db: Session = Depends(get_db)
):

    return delete_machine(
        db,
        machine_id
    )

#Update machine endpoint
@router.put("/machines/{machine_id}")
def edit_machine(
    machine_id: int,
    machine: MachineUpdate,
    db:Session = Depends(get_db)
):
    return update_machine(
        db,
        machine_id,
        machine
        )