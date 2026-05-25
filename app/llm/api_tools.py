import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


# COMMON RESPONSE HANDLER

def handle_response(response):

    # SUCCESS WITH JSON

    if response.content:

        try:

            return response.json()

        except Exception:

            return {
                "success": False,
                "message": response.text
            }

    # SUCCESS WITHOUT BODY

    return {
        "success": True,
        "message": "Operation completed successfully"
    }


# MACHINES

# GET Machines
def get_machines():

    response = requests.get(
        f"{BASE_URL}/machines"
    )

    return handle_response(response)

#GET Machine by ID
def get_machine_by_id(
    machine_id: int
):

    response = requests.get(
        f"{BASE_URL}/machines/{machine_id}"
    )

    return handle_response(response)


# CREATE Machine
def create_machine(
    payload: dict
):

    response = requests.post(

        f"{BASE_URL}/machines",

        json=payload
    )

    return handle_response(response)


# UPDATE Machine
def update_machine(
    machine_id: int,
    payload: dict
):

    response = requests.put(

        f"{BASE_URL}/machines/{machine_id}",

        json=payload
    )

    return handle_response(response)


# DELETE Machine
def delete_machine(
    machine_id: int
):

    response = requests.delete(
        f"{BASE_URL}/machines/{machine_id}"
    )

    if response.status_code in [200, 204]:

        return {
            "success": True,
            "message": f"Machine {machine_id} deleted successfully"
        }

    return handle_response(response)


# MAINTENANCE LOGS

# GET Maintenance Logs
def get_maintenance_logs():

    response = requests.get(
        f"{BASE_URL}/maintenance-logs"
    )

    return handle_response(response)


# GET Maintenance Logs
def get_maintenance_log_by_id(
    maintenance_id: int
):

    response = requests.get(
        f"{BASE_URL}/maintenance-logs/{maintenance_id}"
    )

    return handle_response(response)


# CREATE Maintenance Log
def create_maintenance_log(
    payload: dict
):

    response = requests.post(

        f"{BASE_URL}/maintenance-logs",

        json=payload
    )

    return handle_response(response)


# UPDATE Maintenance Log
def update_maintenance_log(
    maintenance_id: int,
    payload: dict
):

    response = requests.put(

        f"{BASE_URL}/maintenance-logs/{maintenance_id}",

        json=payload
    )

    return handle_response(response)


# DELETE Maintenance Log
def delete_maintenance_log(
    maintenance_id: int
):

    response = requests.delete(
        f"{BASE_URL}/maintenance-logs/{maintenance_id}"
    )

    if response.status_code in [200, 204]:

        return {
            "success": True,
            "message": f"Maintenance log {maintenance_id} deleted successfully"
        }

    return handle_response(response)


# DOWNTIME EVENTS

# GET Downtime Events
def get_downtime_events():

    response = requests.get(
        f"{BASE_URL}/downtime-events"
    )

    return handle_response(response)


# GET Downtime Events by ID
def get_downtime_event_by_id(
    downtime_id: int
):

    response = requests.get(
        f"{BASE_URL}/downtime-events/{downtime_id}"
    )

    return handle_response(response)


# CREATE Downtime Event
def create_downtime_event(
    payload: dict
):

    response = requests.post(

        f"{BASE_URL}/downtime-events",

        json=payload
    )

    return handle_response(response)


# UPDATE Downtime Event
def update_downtime_event(
    downtime_id: int,
    payload: dict
):

    response = requests.put(

        f"{BASE_URL}/downtime-events/{downtime_id}",

        json=payload
    )

    return handle_response(response)


# DELETE Downtime Event
def delete_downtime_events(
    downtime_id: int
):

    response = requests.delete(
        f"{BASE_URL}/downtime-events/{downtime_id}"
    )

    if response.status_code in [200, 204]:

        return {
            "success": True,
            "message": f"Downtime event {downtime_id} deleted successfully"
        }

    return handle_response(response)


# DOWNTIME CAUSES

# GET Downtime Causes
def get_downtime_causes():

    response = requests.get(
        f"{BASE_URL}/downtime-causes"
    )

    return handle_response(response)


# GET Downtime Causes
def get_downtime_cause_by_id(
    cause_id: int
):

    response = requests.get(
        f"{BASE_URL}/downtime-causes/{cause_id}"
    )

    return handle_response(response)


# CREATE Downtime Cause
def create_downtime_cause(
    payload: dict
):

    response = requests.post(

        f"{BASE_URL}/downtime-causes",

        json=payload
    )

    return handle_response(response)


# UPDATE Downtime Cause
def update_downtime_cause(
    cause_id: int,
    payload: dict
):

    response = requests.put(

        f"{BASE_URL}/downtime-causes/{cause_id}",

        json=payload
    )

    return handle_response(response)


# DELETE Downtime Cause
def delete_downtime_causes(
    cause_id: int
):

    response = requests.delete(
        f"{BASE_URL}/downtime-causes/{cause_id}"
    )

    if response.status_code in [200, 204]:

        return {
            "success": True,
            "message": f"Downtime cause {cause_id} deleted successfully"
        }

    return handle_response(response)