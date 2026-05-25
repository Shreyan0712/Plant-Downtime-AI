from mcp.server.fastmcp import FastMCP
import datetime

from app.schemas.machines import(
    MachineCreate
)

from app.llm.api_tools import (

    # MACHINES

    get_machines,
    create_machine,
    update_machine,
    delete_machine,
    get_machine_by_id,


    # MAINTENANCE LOGS

    get_maintenance_logs,
    create_maintenance_log,
    update_maintenance_log,
    delete_maintenance_log,
    get_maintenance_log_by_id,

    # DOWNTIME EVENTS

    get_downtime_events,
    create_downtime_event,
    update_downtime_event,
    delete_downtime_events,
    get_downtime_event_by_id,

    # DOWNTIME CAUSES

    get_downtime_causes,
    create_downtime_cause,
    update_downtime_cause,
    delete_downtime_causes,
    get_downtime_cause_by_id
)



# CREATE MCP SERVER

mcp = FastMCP(
    "Plant Downtime MCP"
)



# ==========================================
# MACHINES TOOLS
# ==========================================

@mcp.tool()
def get_all_machines():

    """
    Retrieve all machine records from the machines table.

    Use this tool when:
    - user asks to show all machines
    - user asks for machine list
    - user asks for machine records
    - user asks to display all machines

    Returns:
    List of all machine records including:
    - machine_id
    - machine_name
    - status
    - location
    - category
    - install_date
    """

    return get_machines()


@mcp.tool()
def get_machine_by_id_tool(
    machine_id: int
):

    """
    Retrieve a machine record using machine ID.

    Use this tool when:
    - user asks for a specific machine
    - user provides a machine ID
    - user asks machine details

    Required fields:
    - machine_id

    Returns:
    Complete machine record for the specified machine ID.
    """

    return get_machine_by_id(machine_id)


@mcp.tool()
def add_machine(

    machine_name: str,

    location: str = None,

    category: str = None,

    install_date: str = None,

    status: str = None
):

    """
    Create a new machine record in the machines table.

    Use this tool when:
    - user wants to add a machine
    - user wants to create a machine record
    - user wants to register a new machine

    Required fields:
    - machine_name

    Optional fields:
    - location
    - category
    - install_date
    - status

    Date format:
    install_date must use:
    YYYY-MM-DD

    Example:
    install_date = 2025-05-22

    Returns:
    Newly created machine record.
    """

    payload = {

        "machine_name": machine_name,

        "location": location,

        "category": category,

        "install_date": install_date,

        "status": status
    }

    return create_machine(payload)


@mcp.tool()
def edit_machine(

    machine_id: int,

    machine_name: str = None,

    location: str = None,

    category: str = None,

    install_date: str = None,

    status: str = None
):

    """
    Update an existing machine record.

    Use this tool when:
    - user wants to update machine details
    - user wants to change machine status
    - user wants to edit machine information

    Required fields:
    - machine_id

    Optional updatable fields:
    - machine_name
    - location
    - category
    - install_date
    - status

    Date format:
    install_date must use:
    YYYY-MM-DD

    Only update fields explicitly mentioned by the user.

    Returns:
    Updated machine record.
    """

    payload = {}

    if machine_name is not None:
        payload["machine_name"] = machine_name

    if location is not None:
        payload["location"] = location

    if category is not None:
        payload["category"] = category

    if install_date is not None:
        payload["install_date"] = install_date

    if status is not None:
        payload["status"] = status

    return update_machine(
        machine_id,
        payload
    )


@mcp.tool()
def remove_machine(
    machine_id: int
):

    """
    Delete a machine record from the machines table.

    Use this tool when:
    - user wants to delete a machine
    - user wants to remove a machine record

    Required fields:
    - machine_id

    Warning:
    This operation permanently deletes the machine record.

    Returns:
    Confirmation of deletion status.
    """

    return delete_machine(machine_id)



# ==========================================
# MAINTENANCE LOGS TOOLS
# ==========================================

@mcp.tool()
def get_all_maintenance_logs():

    """
    Retrieve all maintenance log records.

    Use this tool when:
    - user asks for maintenance logs
    - user asks for maintenance history
    - user asks for servicing records

    Returns:
    List of all maintenance log records.
    """

    return get_maintenance_logs()


@mcp.tool()
def get_maintenance_log_by_id_tool(
    maintenance_id: int
):

    """
    Retrieve a maintenance log using maintenance ID.

    Use this tool when:
    - user asks for a specific maintenance record
    - user provides maintenance ID

    Required fields:
    - maintenance_id

    Returns:
    Complete maintenance log record.
    """

    return get_maintenance_log_by_id(
        maintenance_id
    )


@mcp.tool()
def add_maintenance_log(

    machine_id: int,

    maintenance_type: str,

    start_time: str,

    end_time: str,

    work_done: str,

    technician: str
):

    """
    Create a new maintenance log record.

    Use this tool when:
    - user wants to log maintenance activity
    - user wants to add servicing records
    - user wants to create maintenance history

    Required fields:
    - machine_id
    - maintenance_type
    - start_time
    - end_time
    - work_done
    - technician

    Datetime format:
    Use ISO 8601 format:
    YYYY-MM-DDTHH:MM:SS

    Example:
    2025-01-30T10:00:00

    Returns:
    Newly created maintenance log record.
    """

    payload = {

        "machine_id": machine_id,

        "maintenance_type": maintenance_type,

        "start_time": start_time,

        "end_time": end_time,

        "work_done": work_done,

        "technician": technician
    }

    return create_maintenance_log(payload)


@mcp.tool()
def edit_maintenance_log(

    maintenance_id: int,

    machine_id: int = None,

    maintenance_type: str = None,

    start_time: str = None,

    end_time: str = None,

    work_done: str = None,

    technician: str = None
):

    """
    Update an existing maintenance log.

    Use this tool when:
    - user wants to modify maintenance records
    - user wants to update servicing information

    Required fields:
    - maintenance_id

    Optional updatable fields:
    - machine_id
    - maintenance_type
    - start_time
    - end_time
    - work_done
    - technician

    Datetime format:
    YYYY-MM-DDTHH:MM:SS

    Only update fields explicitly mentioned by the user.

    Returns:
    Updated maintenance log record.
    """

    payload = {}

    if machine_id is not None:
        payload["machine_id"] = machine_id

    if maintenance_type is not None:
        payload["maintenance_type"] = maintenance_type

    if start_time is not None:
        payload["start_time"] = start_time

    if end_time is not None:
        payload["end_time"] = end_time

    if work_done is not None:
        payload["work_done"] = work_done

    if technician is not None:
        payload["technician"] = technician

    return update_maintenance_log(
        maintenance_id,
        payload
    )


@mcp.tool()
def remove_maintenance_log(
    maintenance_id: int
):

    """
    Delete a maintenance log record.

    Use this tool when:
    - user wants to delete maintenance history
    - user wants to remove a maintenance record

    Required fields:
    - maintenance_id

    Warning:
    This operation permanently deletes the record.

    Returns:
    Confirmation of deletion status.
    """

    return delete_maintenance_log(
        maintenance_id
    )



# ==========================================
# DOWNTIME EVENTS TOOLS
# ==========================================

@mcp.tool()
def get_all_downtime_events():

    """
    Retrieve all downtime event records.

    Use this tool when:
    - user asks for downtime events
    - user asks for downtime history
    - user asks for machine stoppage records

    Returns:
    List of downtime event records.
    """

    return get_downtime_events()


@mcp.tool()
def get_downtime_event_by_id_tool(
    downtime_id: int
):

    """
    Retrieve a downtime event using downtime ID.

    Required fields:
    - downtime_id

    Returns:
    Complete downtime event record.
    """

    return get_downtime_event_by_id(
        downtime_id
    )


@mcp.tool()
def add_downtime_event(

    machine_id: int,

    reason_category: str,

    start_time: str,

    end_time: str
):

    """
    Create a downtime event record.

    Use this tool when:
    - user wants to log machine downtime
    - user wants to record stoppage events

    Required fields:
    - machine_id
    - reason_category
    - start_time
    - end_time

    Datetime format:
    YYYY-MM-DDTHH:MM:SS

    Returns:
    Newly created downtime event record.
    """

    payload = {

        "machine_id": machine_id,

        "reason_category": reason_category,

        "start_time": start_time,

        "end_time": end_time
    }

    return create_downtime_event(payload)


@mcp.tool()
def edit_downtime_event(

    downtime_id: int,

    machine_id: int = None,

    reason_category: str = None,

    start_time: str = None,

    end_time: str = None
):

    """
    Update an existing downtime event record.

    Required fields:
    - downtime_id

    Optional updatable fields:
    - machine_id
    - reason_category
    - start_time
    - end_time

    Datetime format:
    YYYY-MM-DDTHH:MM:SS

    Returns:
    Updated downtime event record.
    """

    payload = {}

    if machine_id is not None:
        payload["machine_id"] = machine_id

    if reason_category is not None:
        payload["reason_category"] = reason_category

    if start_time is not None:
        payload["start_time"] = start_time

    if end_time is not None:
        payload["end_time"] = end_time

    return update_downtime_event(
        downtime_id,
        payload
    )


@mcp.tool()
def remove_downtime_event(
    downtime_id: int
):

    """
    Delete a downtime event record.

    Required fields:
    - downtime_id

    Warning:
    This operation permanently deletes the downtime event.

    Returns:
    Confirmation of deletion status.
    """

    return delete_downtime_events(
        downtime_id
    )



# ==========================================
# DOWNTIME CAUSES TOOLS
# ==========================================

@mcp.tool()
def get_all_downtime_causes():

    """
    Retrieve all downtime cause records.

    Use this tool when:
    - user asks for downtime causes
    - user asks for root cause records

    Returns:
    List of downtime cause records.
    """

    return get_downtime_causes()


@mcp.tool()
def get_downtime_cause_by_id_tool(
    cause_id: int
):

    """
    Retrieve a downtime cause using cause ID.

    Required fields:
    - cause_id

    Returns:
    Complete downtime cause record.
    """

    return get_downtime_cause_by_id(
        cause_id
    )


@mcp.tool()
def add_downtime_cause(

    downtime_id: int,

    root_cause: str
):

    """
    Create a downtime cause record.

    Use this tool when:
    - user wants to log root cause analysis
    - user wants to add downtime cause details

    Required fields:
    - downtime_id
    - root_cause

    Returns:
    Newly created downtime cause record.
    """

    payload = {

        "downtime_id": downtime_id,

        "root_cause": root_cause
    }

    return create_downtime_cause(
        payload
    )


@mcp.tool()
def edit_downtime_cause(

    cause_id: int,

    downtime_id: int = None,

    root_cause: str = None
):

    """
    Update a downtime cause record.

    Required fields:
    - cause_id

    Optional updatable fields:
    - downtime_id
    - root_cause

    Returns:
    Updated downtime cause record.
    """

    payload = {}

    if downtime_id is not None:
        payload["downtime_id"] = downtime_id

    if root_cause is not None:
        payload["root_cause"] = root_cause

    return update_downtime_cause(
        cause_id,
        payload
    )


@mcp.tool()
def remove_downtime_cause(
    cause_id: int
):

    """
    Delete a downtime cause record.

    Required fields:
    - cause_id

    Warning:
    This operation permanently deletes the record.

    Returns:
    Confirmation of deletion status.
    """

    return delete_downtime_causes(
        cause_id
    )


# RUN MCP SERVER

if __name__ == "__main__":

    mcp.run()