from mcp.server.fastmcp import FastMCP

from app.schemas.machines import MachineCreate

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
    get_downtime_cause_by_id,
)


mcp = FastMCP("Plant Downtime MCP")


# helper: normalise an api_tools response to a list of dict rows
def _rows(payload):
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if isinstance(payload, dict) and payload.get("success") is not False:
        return [payload]
    return []


# ==========================================
# MACHINES TOOLS
# ==========================================
@mcp.tool()
def get_all_machines():
    """
    Retrieve all machine records. Use only when the user wants the full machine list.
    For acting on a machine by name, prefer find_machines_by_name.
    """
    return get_machines()


@mcp.tool()
def find_machines_by_name(name: str):
    """
    Find machines whose name contains the given text (case-insensitive).
    Returns an empty list if name is blank — use get_all_machines for the full list.
    """
    name_l = (name or "").strip().lower()
    if not name_l:
        return {"success": False, "message": "find_machines_by_name requires a non-empty name; use get_all_machines for the full list."}
    return [
        m for m in _rows(get_machines())
        if name_l in str(m.get("machine_name", "")).lower()
    ]


@mcp.tool()
def get_machine_by_id_tool(machine_id: int):
    """
    Retrieve a single machine record by machine ID.

    Required:
    - machine_id
    """
    return get_machine_by_id(machine_id)


@mcp.tool()
def add_machine(
    machine_name: str,
    location: str = None,
    category: str = None,
    install_date: str = None,
    status: str = None,
):
    """
    Create a new machine record.

    Required: machine_name
    Optional: location, category, install_date (YYYY-MM-DD), status
    """
    payload = {
        "machine_name": machine_name,
        "location": location,
        "category": category,
        "install_date": install_date,
        "status": status,
    }
    return create_machine(payload)


@mcp.tool()
def edit_machine(
    machine_id: int,
    machine_name: str = None,
    location: str = None,
    category: str = None,
    install_date: str = None,
    status: str = None,
):
    """
    Update an existing machine. Required: machine_id.
    Only update fields explicitly mentioned. install_date: YYYY-MM-DD.
    """
    payload = {}
    if machine_name is not None: payload["machine_name"] = machine_name
    if location is not None: payload["location"] = location
    if category is not None: payload["category"] = category
    if install_date is not None: payload["install_date"] = install_date
    if status is not None: payload["status"] = status
    return update_machine(machine_id, payload)


@mcp.tool()
def remove_machine(machine_id: int):
    """
    Delete a machine record. Required: machine_id. Permanent.
    """
    return delete_machine(machine_id)


# ==========================================
# MAINTENANCE LOGS TOOLS
# ==========================================
@mcp.tool()
def get_all_maintenance_logs():
    """
    Retrieve all maintenance logs. For logs of one machine, prefer find_maintenance_by_machine.
    """
    return get_maintenance_logs()


@mcp.tool()
def find_maintenance_by_machine(machine_id: int):
    """
    Find maintenance logs for a specific machine_id.
    Returns an error if machine_id is missing — use get_all_maintenance_logs for the full list.

    Required:
    - machine_id (must be a positive integer)
    """
    if not machine_id or machine_id <= 0:
        return {"success": False, "message": "find_maintenance_by_machine requires a valid machine_id. Use get_all_maintenance_logs for the full list."}
    return [
        m for m in _rows(get_maintenance_logs())
        if str(m.get("machine_id")) == str(machine_id)
    ]


@mcp.tool()
def get_maintenance_log_by_id_tool(maintenance_id: int):
    """
    Retrieve a single maintenance log by maintenance_id.
    """
    return get_maintenance_log_by_id(maintenance_id)


@mcp.tool()
def add_maintenance_log(
    machine_id: int,
    maintenance_type: str,
    start_time: str,
    end_time: str,
    work_done: str,
    technician: str,
):
    """
    Create a maintenance log.
    Required: machine_id, maintenance_type, start_time, end_time, work_done, technician.
    Datetime format: YYYY-MM-DDTHH:MM:SS
    """
    payload = {
        "machine_id": machine_id,
        "maintenance_type": maintenance_type,
        "start_time": start_time,
        "end_time": end_time,
        "work_done": work_done,
        "technician": technician,
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
    technician: str = None,
):
    """
    Update a maintenance log. Required: maintenance_id.
    Only update mentioned fields. Datetime: YYYY-MM-DDTHH:MM:SS
    """
    payload = {}
    if machine_id is not None: payload["machine_id"] = machine_id
    if maintenance_type is not None: payload["maintenance_type"] = maintenance_type
    if start_time is not None: payload["start_time"] = start_time
    if end_time is not None: payload["end_time"] = end_time
    if work_done is not None: payload["work_done"] = work_done
    if technician is not None: payload["technician"] = technician
    return update_maintenance_log(maintenance_id, payload)


@mcp.tool()
def remove_maintenance_log(maintenance_id: int):
    """
    Delete a maintenance log. Required: maintenance_id. Permanent.
    """
    return delete_maintenance_log(maintenance_id)


# ==========================================
# DOWNTIME EVENTS TOOLS
# ==========================================
@mcp.tool()
def get_all_downtime_events():
    """
    Retrieve all downtime events. For events of one machine, prefer find_downtime_by_machine.
    """
    return get_downtime_events()


@mcp.tool()
def find_downtime_by_machine(machine_id: int):
    """
    Find downtime events for a specific machine_id.
    Returns an error if machine_id is missing — use get_all_downtime_events for the full list.

    Required:
    - machine_id (must be a positive integer)
    """
    if not machine_id or machine_id <= 0:
        return {"success": False, "message": "find_downtime_by_machine requires a valid machine_id. Use get_all_downtime_events for the full list."}
    return [
        d for d in _rows(get_downtime_events())
        if str(d.get("machine_id")) == str(machine_id)
    ]



@mcp.tool()
def get_downtime_event_by_id_tool(downtime_id: int):
    """
    Retrieve a single downtime event by downtime_id.
    """
    return get_downtime_event_by_id(downtime_id)


@mcp.tool()
def add_downtime_event(
    machine_id: int,
    reason_category: str,
    start_time: str,
    end_time: str,
):
    """
    Create a downtime event.
    Required: machine_id, reason_category, start_time, end_time.
    Datetime: YYYY-MM-DDTHH:MM:SS
    """
    payload = {
        "machine_id": machine_id,
        "reason_category": reason_category,
        "start_time": start_time,
        "end_time": end_time,
    }
    return create_downtime_event(payload)


@mcp.tool()
def edit_downtime_event(
    downtime_id: int,
    machine_id: int = None,
    reason_category: str = None,
    start_time: str = None,
    end_time: str = None,
):
    """
    Update a downtime event. Required: downtime_id.
    Datetime: YYYY-MM-DDTHH:MM:SS
    """
    payload = {}
    if machine_id is not None: payload["machine_id"] = machine_id
    if reason_category is not None: payload["reason_category"] = reason_category
    if start_time is not None: payload["start_time"] = start_time
    if end_time is not None: payload["end_time"] = end_time
    return update_downtime_event(downtime_id, payload)


@mcp.tool()
def remove_downtime_event(downtime_id: int):
    """
    Delete a downtime event. Required: downtime_id. Permanent.
    """
    return delete_downtime_events(downtime_id)


# ==========================================
# DOWNTIME CAUSES TOOLS
# ==========================================
@mcp.tool()
def get_all_downtime_causes():
    """
    Retrieve all downtime causes. For causes of one downtime event, prefer
    find_causes_by_downtime.
    """
    return get_downtime_causes()


@mcp.tool()
def find_causes_by_downtime(downtime_id: int):
    """
    Find downtime causes linked to a specific downtime_id.
    Returns an error if downtime_id is missing — use get_all_downtime_causes for the full list.

    Required:
    - downtime_id (must be a positive integer)
    """
    if not downtime_id or downtime_id <= 0:
        return {"success": False, "message": "find_causes_by_downtime requires a valid downtime_id. Use get_all_downtime_causes for the full list."}
    return [
        c for c in _rows(get_downtime_causes())
        if str(c.get("downtime_id")) == str(downtime_id)
    ]


@mcp.tool()
def get_downtime_cause_by_id_tool(cause_id: int):
    """
    Retrieve a single downtime cause by cause_id.
    """
    return get_downtime_cause_by_id(cause_id)


@mcp.tool()
def add_downtime_cause(downtime_id: int, root_cause: str):
    """
    Create a downtime cause.
    Required: downtime_id, root_cause.
    """
    payload = {"downtime_id": downtime_id, "root_cause": root_cause}
    return create_downtime_cause(payload)


@mcp.tool()
def edit_downtime_cause(
    cause_id: int,
    downtime_id: int = None,
    root_cause: str = None,
):
    """
    Update a downtime cause. Required: cause_id.
    """
    payload = {}
    if downtime_id is not None: payload["downtime_id"] = downtime_id
    if root_cause is not None: payload["root_cause"] = root_cause
    return update_downtime_cause(cause_id, payload)


@mcp.tool()
def remove_downtime_cause(cause_id: int):
    """
    Delete a downtime cause. Required: cause_id. Permanent.
    """
    return delete_downtime_causes(cause_id)


# RUN MCP SERVER
if __name__ == "__main__":
    mcp.run()