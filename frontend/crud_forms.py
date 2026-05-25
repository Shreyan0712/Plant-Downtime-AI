"""
crud_forms.py — Add / Update / Delete form pages for each table.

Each render_*_page() draws three tabs (Add, Update, Delete) and calls the
CRUD wrappers in workspace.py, which post to your FastAPI backend.

Field names and payload shapes match your Pydantic schemas exactly:
  MachineCreate, MaintenanceLogCreate, DowntimeEventCreate, DowntimeCauseCreate.
Datetimes are sent as ISO strings (YYYY-MM-DDTHH:MM:SS); dates as YYYY-MM-DD.
"""

from __future__ import annotations

import datetime as dt
import streamlit as st

import frontend.workspace as ws

def _refresh(builder):
    """Re-fresh a table and store it as the current workspace view."""
    st.session_state.view = builder()

def _dt(date_val, time_str: str = "00:00:00") -> str | None:
    if not date_val:
        return None
    return f"{date_val.isoformat()}T{time_str}"


def _confirm_delete(label: str) -> bool:
    return st.checkbox(f"I understand deleting {label} is permanent.")


# MACHINES
def render_machines_page():
    st.subheader("Machines — Add / Update / Delete")
    add, upd, dele = st.tabs(["➕ Add", "✏️ Update", "🗑️ Delete"])

    with add:
        with st.form("m_add", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Machine Name *")
            status = c2.selectbox("Status", ["Running", "Idle", "Down", "Maintenance"])
            location = c1.text_input("Location")
            category = c2.text_input("Category")
            install = c1.date_input("Install Date", value=None)
            if st.form_submit_button("Add Machine", use_container_width=True):
                if not name.strip():
                    st.warning("Machine Name is required.")
                else:
                    payload = {"machine_name": name, "status": status,
                               "location": location or None, "category": category or None,
                               "install_date": install.isoformat() if install else None}
                    st.success(ws.create_machine(payload))
                    _refresh(ws.build_machines)

    with upd:
        with st.form("m_upd", clear_on_submit=False):
            mid = st.number_input("Machine ID to update *", min_value=1, step=1)
            st.caption("Leave a field blank to keep it unchanged.")
            c1, c2 = st.columns(2)
            name = c1.text_input("Machine Name")
            status = c2.selectbox("Status", ["", "Running", "Idle", "Down", "Maintenance"])
            location = c1.text_input("Location")
            category = c2.text_input("Category")
            install = c1.date_input("Install Date", value=None)
            if st.form_submit_button("Update Machine", use_container_width=True):
                payload = {k: v for k, v in {
                    "machine_name": name or None, "status": status or None,
                    "location": location or None, "category": category or None,
                    "install_date": install.isoformat() if install else None,
                }.items() if v is not None}
                st.success(ws.update_machine(int(mid), payload))
                _refresh(ws.build_machines)

    with dele:
        mid = st.number_input("Machine ID to delete *", min_value=1, step=1, key="m_del")
        ok = _confirm_delete(f"machine {int(mid)}")
        if st.button("Delete Machine", use_container_width=True, disabled=not ok):
            st.success(ws.delete_machine(int(mid)))
            _refresh(ws.build_machines)


# MAINTENANCE LOGS
def render_maintenance_page():
    st.subheader("Maintenance Logs — Add / Update / Delete")
    add, upd, dele = st.tabs(["➕ Add", "✏️ Update", "🗑️ Delete"])

    types = ["Planned", "Unplanned", "Servicing", "Repair", "Inspection", "Calibration"]

    with add:
        with st.form("t_add", clear_on_submit=True):
            c1, c2 = st.columns(2)
            machine_id = c1.number_input("Machine ID *", min_value=1, step=1)
            mtype = c2.selectbox("Maintenance Type", types)
            start_d = c1.date_input("Start Date", value=None)
            end_d = c2.date_input("End Date", value=None)
            technician = c1.text_input("Technician")
            work_done = c2.text_input("Work Done")
            if st.form_submit_button("Add Log", use_container_width=True):
                payload = {"machine_id": int(machine_id), "maintenance_type": mtype,
                           "start_time": _dt(start_d), "end_time": _dt(end_d),
                           "technician": technician or None, "work_done": work_done or None}
                st.success(ws.create_maintenance(payload))
                _refresh(ws.build_maintenance)

    with upd:
        with st.form("t_upd", clear_on_submit=False):
            log_id = st.number_input("Maintenance ID to update *", min_value=1, step=1)
            machine_id = st.number_input("Machine ID *", min_value=1, step=1)
            c1, c2 = st.columns(2)
            mtype = c1.selectbox("Maintenance Type", [""] + types)
            technician = c2.text_input("Technician")
            start_d = c1.date_input("Start Date", value=None)
            end_d = c2.date_input("End Date", value=None)
            work_done = st.text_input("Work Done")
            if st.form_submit_button("Update Log", use_container_width=True):
                payload = {"machine_id": int(machine_id)}
                if mtype: payload["maintenance_type"] = mtype
                if technician: payload["technician"] = technician
                if work_done: payload["work_done"] = work_done
                if start_d: payload["start_time"] = _dt(start_d)
                if end_d: payload["end_time"] = _dt(end_d)
                st.success(ws.update_maintenance(int(log_id), payload))
                _refresh(ws.build_maintenance)

    with dele:
        log_id = st.number_input("Maintenance ID to delete *", min_value=1, step=1, key="t_del")
        ok = _confirm_delete(f"maintenance log {int(log_id)}")
        if st.button("Delete Log", use_container_width=True, disabled=not ok):
            st.success(ws.delete_maintenance(int(log_id)))
            _refresh(ws.build_maintenance)


# DOWNTIME EVENTS
def render_downtime_page():
    st.subheader("Downtime Events — Add / Update / Delete")
    add, upd, dele = st.tabs(["➕ Add", "✏️ Update", "🗑️ Delete"])

    with add:
        with st.form("d_add", clear_on_submit=True):
            c1, c2 = st.columns(2)
            machine_id = c1.number_input("Machine ID *", min_value=1, step=1)
            minutes = c2.number_input("Downtime Minutes", min_value=0, step=5)
            start_d = c1.date_input("Start Date *")
            end_d = c2.date_input("End Date", value=None)
            reason_cat = c1.text_input("Reason Category")
            reason_det = c2.text_input("Reason Details")
            reported_by = c1.text_input("Reported By")
            if st.form_submit_button("Add Event", use_container_width=True):
                payload = {"machine_id": int(machine_id),
                           "start_time": _dt(start_d), "end_time": _dt(end_d),
                           "downtime_minutes": int(minutes) or None,
                           "reason_category": reason_cat or None,
                           "reason_details": reason_det or None,
                           "reported_by": reported_by or None}
                st.success(ws.create_downtime(payload))
                _refresh(ws.build_downtime)

    with upd:
        with st.form("d_upd", clear_on_submit=False):
            dtid = st.number_input("Downtime ID to update *", min_value=1, step=1)
            machine_id = st.number_input("Machine ID *", min_value=1, step=1)
            start_d = st.date_input("Start Date *")
            c1, c2 = st.columns(2)
            end_d = c1.date_input("End Date", value=None)
            minutes = c2.number_input("Downtime Minutes", min_value=0, step=5)
            reason_cat = c1.text_input("Reason Category")
            reason_det = c2.text_input("Reason Details")
            reported_by = st.text_input("Reported By")
            if st.form_submit_button("Update Event", use_container_width=True):
                payload = {"machine_id": int(machine_id), "start_time": _dt(start_d)}
                if end_d: payload["end_time"] = _dt(end_d)
                if minutes: payload["downtime_minutes"] = int(minutes)
                if reason_cat: payload["reason_category"] = reason_cat
                if reason_det: payload["reason_details"] = reason_det
                if reported_by: payload["reported_by"] = reported_by
                st.success(ws.update_downtime(int(dtid), payload))
                _refresh(ws.build_downtime)

    with dele:
        dtid = st.number_input("Downtime ID to delete *", min_value=1, step=1, key="d_del")
        ok = _confirm_delete(f"downtime event {int(dtid)}")
        if st.button("Delete Event", use_container_width=True, disabled=not ok):
            st.success(ws.delete_downtime(int(dtid)))
            _refresh(ws.build_downtime)


# DOWNTIME CAUSES
def render_causes_page():
    st.subheader("Downtime Causes — Add / Update / Delete")
    add, upd, dele = st.tabs(["➕ Add", "✏️ Update", "🗑️ Delete"])

    with add:
        with st.form("c_add", clear_on_submit=True):
            c1, c2 = st.columns(2)
            downtime_id = c1.number_input("Downtime ID *", min_value=1, step=1)
            category = c2.text_input("Category")
            root_cause = st.text_input("Root Cause")
            corrective = st.text_area("Corrective Action")
            preventive = st.text_area("Preventive Action")
            if st.form_submit_button("Add Cause", use_container_width=True):
                payload = {"downtime_id": int(downtime_id),
                           "root_cause": root_cause or None, "category": category or None,
                           "corrective_action": corrective or None,
                           "preventive_action": preventive or None}
                st.success(ws.create_cause(payload))
                _refresh(ws.build_causes)

    with upd:
        with st.form("c_upd", clear_on_submit=False):
            cid = st.number_input("Cause ID to update *", min_value=1, step=1)
            downtime_id = st.number_input("Downtime ID *", min_value=1, step=1)
            category = st.text_input("Category")
            root_cause = st.text_input("Root Cause")
            corrective = st.text_area("Corrective Action")
            preventive = st.text_area("Preventive Action")
            if st.form_submit_button("Update Cause", use_container_width=True):
                payload = {"downtime_id": int(downtime_id)}
                if category: payload["category"] = category
                if root_cause: payload["root_cause"] = root_cause
                if corrective: payload["corrective_action"] = corrective
                if preventive: payload["preventive_action"] = preventive
                st.success(ws.update_cause(int(cid), payload))
                _refresh(ws.build_causes)

    with dele:
        cid = st.number_input("Cause ID to delete *", min_value=1, step=1, key="c_del")
        ok = _confirm_delete(f"downtime cause {int(cid)}")
        if st.button("Delete Cause", use_container_width=True, disabled=not ok):
            st.success(ws.delete_cause(int(cid)))
            _refresh(ws.build_causes)


# router used by frontend_app.py
PAGES = {
    "machines": render_machines_page,
    "maintenance": render_maintenance_page,
    "downtime": render_downtime_page,
    "causes": render_causes_page,
}