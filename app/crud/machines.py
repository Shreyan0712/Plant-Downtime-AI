from sqlalchemy.orm import Session
from app.models.models import Machines
from app.schemas.machines import (
    MachineCreate,
    MachineUpdate
)

#Get all machines
def get_all_machines(db:Session):
    return db.query(Machines).all()

#Get by machine id
def get_machine_by_id(
    db:Session,
    machine_id: int
    ):
    return db.query(Machines).filter(
        Machines.machine_id == machine_id
    ).first()

#Create machine
def create_machine(
    db:Session,
    machine: MachineCreate
):
    
    db_machine = Machines(
        machine_name = machine.machine_name,
        location = machine.location,
        category = machine.category,
        install_date = machine.install_date,
        status = machine.status
    )

    db.add(db_machine)

    db.commit()

    db.refresh(db_machine)

    return db_machine

#Delete machine by machine_id
def delete_machine(
    db: Session,
    machine_id: int
):
    machine = db.query(Machines).filter(
        Machines.machine_id == machine_id
    ).first()

    if machine:

        db.delete(machine)

        db.commit()

    return machine

#Update machine by machine_id
# Update machine by machine_id
def update_machine(
    db: Session,
    machine_id: int,
    machine_data: MachineUpdate
):

    machine = db.query(Machines).filter(
        Machines.machine_id == machine_id
    ).first()

    if not machine:

        return None

    # ONLY UPDATE PROVIDED FIELDS

    if machine_data.machine_name is not None:
        machine.machine_name = machine_data.machine_name

    if machine_data.location is not None:
        machine.location = machine_data.location

    if machine_data.category is not None:
        machine.category = machine_data.category

    if machine_data.install_date is not None:
        machine.install_date = machine_data.install_date

    if machine_data.status is not None:
        machine.status = machine_data.status

    db.commit()

    db.refresh(machine)

    return machine
