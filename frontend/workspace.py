"""
workspace.py — data layer for the Plant Downtime AI frontend.

Pulls real records from the FastAPI backend (app.llm.api_tools), builds a
WorkspaceView (table + stat cards + colorful Plotly charts), routes chat
messages, and exposes thin CRUD wrappers used by the form pages.

Falls back to small demo datasets if the API is unreachable, so the UI never
goes blank.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.llm import api_tools
from app.llm.agent import run_agent


# THEME (shared by all charts)
PALETTE = ["#2dd4bf", "#5b9dff", "#f5a524", "#a78bfa", "#34d399",
           "#f87171", "#22d3ee", "#fb923c", "#c084fc", "#4ade80"]


def _style(fig: go.Figure, height: int = 360) -> go.Figure:
    """Apply a consistent dark, colorful style to a Plotly figure."""
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e7ecf5", size=13),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        showlegend=False,
        bargap=0.25,
    )
    return fig


# DATA MODEL
@dataclass
class InfoBox:
    title: str
    stat: str
    body: str = ""


@dataclass
class Chart:
    title: str
    figure: go.Figure


@dataclass
class WorkspaceView:
    title: str = "Workspace"
    table: Optional[pd.DataFrame] = None
    info_boxes: list[InfoBox] = field(default_factory=list)
    charts: list[Chart] = field(default_factory=list)
    chat_reply: str = ""


# HELPERS
def as_records(payload) -> list[dict]:
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if isinstance(payload, dict):
        if payload.get("success") is False:
            return []
        for key in ("data", "results", "items", "records"):
            if isinstance(payload.get(key), list):
                return payload[key]
        if payload and "message" not in payload:
            return [payload]
    return []


def pretty(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    return df.rename(columns={c: c.replace("_", " ").title() for c in df.columns})


def _num(series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0)


def _bar_from_counts(series, value_name: str) -> go.Figure:
    """Colorful bar chart from a categorical column's value_counts."""
    vc = series.fillna("Unknown").value_counts()
    fig = px.bar(
        x=vc.index.astype(str), y=vc.values,
        color=vc.index.astype(str),
        color_discrete_sequence=PALETTE,
        text=vc.values,
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis_title="", yaxis_title=value_name)
    return _style(fig)


def _bar_from_series(idx, values, value_name: str) -> go.Figure:
    fig = px.bar(
        x=[str(i) for i in idx], y=list(values),
        color=[str(i) for i in idx],
        color_discrete_sequence=PALETTE,
        text=[round(v, 1) for v in values],
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis_title="", yaxis_title=value_name)
    return _style(fig)


def _pie_from_counts(series) -> go.Figure:
    vc = series.fillna("Unknown").value_counts()
    fig = px.pie(
        names=vc.index.astype(str), values=vc.values, hole=0.45,
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True,
                      legend=dict(font=dict(color="#e7ecf5")))
    return _style(fig)


# DEMO FALLBACKS
_DEMO_MACHINES = [
    {"machine_id": 1, "machine_name": "Lathe Machine A", "status": "Running", "location": "Line 1", "category": "Lathe"},
    {"machine_id": 2, "machine_name": "CNC Mill B", "status": "Idle", "location": "Line 2", "category": "CNC"},
    {"machine_id": 3, "machine_name": "Hydraulic Press", "status": "Down", "location": "Line 2", "category": "Press"},
    {"machine_id": 4, "machine_name": "Conveyor 3", "status": "Running", "location": "Line 3", "category": "Conveyor"},
]
_DEMO_MAINT = [
    {"maintenance_id": 21, "machine_id": 2, "maintenance_type": "Planned", "technician": "Tech X"},
    {"maintenance_id": 22, "machine_id": 3, "maintenance_type": "Unplanned", "technician": "Tech Y"},
    {"maintenance_id": 23, "machine_id": 1, "maintenance_type": "Planned", "technician": "Tech X"},
]
_DEMO_DOWNTIME = [
    {"downtime_id": 1, "machine_id": 3, "downtime_minutes": 120, "reason_category": "Mechanical"},
    {"downtime_id": 2, "machine_id": 2, "downtime_minutes": 75, "reason_category": "Electrical"},
    {"downtime_id": 3, "machine_id": 3, "downtime_minutes": 45, "reason_category": "Mechanical"},
]
_DEMO_CAUSES = [
    {"cause_id": 1, "downtime_id": 1, "category": "Wear", "root_cause": "Bearing failure", "preventive_action": "Lubrication schedule"},
    {"cause_id": 2, "downtime_id": 2, "category": "Power", "root_cause": "Fuse blown", "preventive_action": "Surge protection"},
]


def _fetch(get_fn, demo: list[dict]) -> tuple[pd.DataFrame, bool]:
    try:
        records = as_records(get_fn())
    except Exception:
        records = []
    if records:
        return pd.DataFrame(records), True
    return pd.DataFrame(demo), False


# VIEW BUILDERS
def build_machines() -> WorkspaceView:
    df, live = _fetch(api_tools.get_machines, _DEMO_MACHINES)
    status = df.get("status", pd.Series(dtype=str)).fillna("Unknown")
    not_running = int(status.str.lower().isin(["down", "idle", "stopped", "maintenance"]).sum())
    running = int(status.str.lower().eq("running").sum())

    boxes = [
        InfoBox("Total Machines", str(len(df)), f"{running} running · {not_running} not running"),
        InfoBox("Running", str(running), "Currently operational"),
        InfoBox("Not Running", str(not_running), "Idle / down / maintenance"),
        InfoBox("Categories", str(df["category"].nunique()) if "category" in df else "0", "Distinct machine types"),
    ]
    charts = []
    if "status" in df:
        charts.append(Chart("Machines by Status", _pie_from_counts(df["status"])))
    if "category" in df:
        charts.append(Chart("Machines by Category", _bar_from_counts(df["category"], "Machines")))

    return WorkspaceView("Machines", pretty(df), boxes, charts, _reply(len(df), "machine", live))


def build_maintenance() -> WorkspaceView:
    df, live = _fetch(api_tools.get_maintenance_logs, _DEMO_MAINT)
    mtype = df.get("maintenance_type", pd.Series(dtype=str)).fillna("Unspecified")
    top_type = mtype.mode().iloc[0] if not mtype.mode().empty else "-"
    techs = df["technician"].nunique() if "technician" in df else 0

    boxes = [
        InfoBox("Total Logs", str(len(df)), "Maintenance records"),
        InfoBox("Most Common", str(top_type), "Maintenance type"),
        InfoBox("Technicians", str(techs), "Distinct technicians"),
        InfoBox("Machines Covered", str(df["machine_id"].nunique()) if "machine_id" in df else "0", "Serviced machines"),
    ]
    charts = []
    if "maintenance_type" in df:
        charts.append(Chart("Logs by Type", _pie_from_counts(df["maintenance_type"])))
    if "technician" in df:
        top = df["technician"].fillna("Unknown").value_counts().head(10)
        charts.append(Chart("Logs by Technician (top 10)",
                            _bar_from_series(top.index, top.values, "Logs")))

    return WorkspaceView("Maintenance Logs", pretty(df), boxes, charts, _reply(len(df), "maintenance log", live))


def build_downtime() -> WorkspaceView:
    df, live = _fetch(api_tools.get_downtime_events, _DEMO_DOWNTIME)
    minutes = _num(df.get("downtime_minutes", pd.Series(dtype=float)))
    total = int(minutes.sum())
    top_reason = "-"
    if "reason_category" in df and not df["reason_category"].dropna().empty:
        top_reason = df["reason_category"].mode().iloc[0]
    worst = "-"
    if "machine_id" in df and not df["machine_id"].dropna().empty:
        worst = str(df["machine_id"].value_counts().idxmax())

    boxes = [
        InfoBox("Events", str(len(df)), "Downtime incidents"),
        InfoBox("Total Downtime", f"{total} min", f"~{total/60:.1f} hours"),
        InfoBox("Top Reason", str(top_reason), "Most frequent category"),
        InfoBox("Worst Machine", worst, "Most downtime events"),
    ]
    charts = []
    if "reason_category" in df:
        charts.append(Chart("Downtime by Reason", _pie_from_counts(df["reason_category"])))
    if "machine_id" in df and "downtime_minutes" in df:
        tmp = df.copy()
        tmp["downtime_minutes"] = _num(tmp["downtime_minutes"])
        by_machine = tmp.groupby("machine_id")["downtime_minutes"].sum().sort_values(ascending=False).head(10)
        labels = [f"Machine {m}" for m in by_machine.index]
        charts.append(Chart("Total Downtime Minutes by Machine (top 10)",
                            _bar_from_series(labels, by_machine.values, "Minutes")))

    return WorkspaceView("Downtime Events", pretty(df), boxes, charts, _reply(len(df), "downtime event", live))


def build_causes() -> WorkspaceView:
    df, live = _fetch(api_tools.get_downtime_causes, _DEMO_CAUSES)
    cat = df.get("category", pd.Series(dtype=str)).fillna("Uncategorised")
    top_cat = cat.mode().iloc[0] if not cat.mode().empty else "-"
    with_prev = int(df["preventive_action"].notna().sum()) if "preventive_action" in df else 0

    boxes = [
        InfoBox("Total Causes", str(len(df)), "Root-cause records"),
        InfoBox("Categories", str(cat.nunique()), f"Top: {top_cat}"),
        InfoBox("With Preventive", str(with_prev), "Have a preventive action"),
        InfoBox("Events Linked", str(df["downtime_id"].nunique()) if "downtime_id" in df else "0", "Distinct events"),
    ]
    charts = []
    if "category" in df:
        charts.append(Chart("Causes by Category", _bar_from_counts(df["category"], "Causes")))

    return WorkspaceView("Downtime Causes", pretty(df), boxes, charts, _reply(len(df), "downtime cause", live))


def _reply(n: int, noun: str, live: bool) -> str:
    src = "" if live else " (demo data — API not reachable)"
    return f"Loaded {n} {noun}(s) into the workspace{src}."


# CHAT ROUTER
_INTENTS = [
    (("maintenance", "service", "servicing", "repair log"), build_maintenance),
    (("cause", "root cause", "corrective", "preventive"),   build_causes),
    (("downtime", "outage", "stoppage", "breakdown"),        build_downtime),
    (("machine", "equipment", "asset"),                      build_machines),
]
_DISPLAY_VERBS = ("show", "display", "list", "get", "view", "see", "fetch", "pull", "load", "give me", "what are")
_WRITE_VERBS = {"add", "create", "insert", "new", "update", "edit", "change", "modify",
                "set", "delete", "remove", "drop"}

def _builder_for(text: str):
    """Return the build_* function for whichever table the message mentions"""
    for keywords, builder in _INTENTS:
        if any(k in text for k in keywords):
            return builder
    return None

def route_message(message: str):
    """
    Always let the LLM agent answer (dynamic, natural-language reply).
    Separately, decide wether the workspace table should refresh.
    Returns (view_or_none, reply_text) 
    """

    text = message.lower()

    #Actual conversation handled by LLM
    reply = run_agent(message)

    #Decide wether to refresh workspace table
    builder = _builder_for(text)
    is_display = any(v in text for v in _DISPLAY_VERBS)
    is_write = any(v in text for v in _WRITE_VERBS)


    if builder is not None and (is_display or is_write):
        view = builder()
        return view, reply
    
    return None, reply


# CRUD WRAPPERS  (used by crud_forms.py)
def _msg(result) -> str:
    if isinstance(result, dict):
        return result.get("message") or "Done."
    return "Done."


# -- machines --
def create_machine(payload):  return _msg(api_tools.create_machine(payload))
def update_machine(mid, p):   return _msg(api_tools.update_machine(mid, p))
def delete_machine(mid):      return _msg(api_tools.delete_machine(mid))

# -- maintenance --
def create_maintenance(p):    return _msg(api_tools.create_maintenance_log(p))
def update_maintenance(i, p): return _msg(api_tools.update_maintenance_log(i, p))
def delete_maintenance(i):    return _msg(api_tools.delete_maintenance_log(i))

# -- downtime events --
def create_downtime(p):       return _msg(api_tools.create_downtime_event(p))
def update_downtime(i, p):    return _msg(api_tools.update_downtime_event(i, p))
def delete_downtime(i):       return _msg(api_tools.delete_downtime_events(i))

# -- downtime causes --
def create_cause(p):          return _msg(api_tools.create_downtime_cause(p))
def update_cause(i, p):       return _msg(api_tools.update_downtime_cause(i, p))
def delete_cause(i):          return _msg(api_tools.delete_downtime_causes(i))