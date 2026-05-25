"""
Plant Downtime AI - Frontend (functional build)
================================================

Sidebar:
    Workspace          -> table + stat cards + colorful charts
    Machines           -> CRUD form page
    Maintenance Logs   -> CRUD form page
    Downtime Events    -> CRUD form page
    Downtime Causes    -> CRUD form page

Run order (TWO terminals, from project root C:\\Internship\\Plant_Downtime_API):
    1)  uvicorn app.main:app --reload      (BASE_URL in .env must point to it)
    2)  streamlit run frontend_app.py
Requires plotly:  pip install plotly
"""

from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

import frontend.workspace as ws
import frontend.crud_forms as crud_forms


# PAGE CONFIG
st.set_page_config(page_title="Plant Downtime AI", page_icon="🏭", layout="wide")

st.markdown(
    """
    <style>
      .block-container { padding-top: 1.5rem !important; }
      .scroll-row { display: flex; gap: 16px; overflow-x: auto; padding: 6px 2px 14px 2px; }
      .scroll-row::-webkit-scrollbar { height: 8px; }
      .scroll-row::-webkit-scrollbar-thumb { background: #c7ced9; border-radius: 4px; }
      .info-box {
        flex: 0 0 280px; min-height: 150px;
        background: #f5f7fb; border: 1px solid #dfe5ee; border-radius: 14px;
        padding: 14px 16px; box-sizing: border-box;
      }
      .info-box .box-title { font-weight: 700; font-size: 14px; color: #1f2937; margin-bottom: 6px; }
      .info-box .big-stat  { font-size: 30px; font-weight: 800; color: #0e7c6b; }
      .info-box .box-body  { font-size: 13px; color: #5b6573; line-height: 1.35; }
      .panel-label { font-weight: 700; font-size: 15px; color: #1f2937; margin: 2px 0 8px 0; }
      .charts-label { font-weight: 700; font-size: 16px; color: #e7ecf5; margin: 16px 0 8px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
if "view" not in st.session_state:
    st.session_state.view = ws.build_machines()
if "page" not in st.session_state:
    st.session_state.page = "workspace"


def go(page: str):
    st.session_state.page = page
    st.rerun()


# SIDEBAR
with st.sidebar:
    st.markdown("### 🏭 Plant Downtime")
    st.caption("AI Workspace")
    st.divider()
    if st.button("📊 Workspace", use_container_width=True):
        go("workspace")
    st.markdown("**Manage Tables**")
    if st.button("Machines", use_container_width=True):
        go("machines")
    if st.button("Maintenance Logs", use_container_width=True):
        go("maintenance")
    if st.button("Downtime Events", use_container_width=True):
        go("downtime")
    if st.button("Downtime Causes", use_container_width=True):
        go("causes")
    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# CRUD FORM PAGES
if st.session_state.page in crud_forms.PAGES:
    st.write("")
    st.write("")
    if st.button("← Back to Workspace"):
        go("workspace")
    crud_forms.PAGES[st.session_state.page]()
    st.stop()


# WORKSPACE PAGE  ->  [ workspace | chat box ]
st.markdown("# 🏭 Plant Downtime AI — Workspace")

main_col, chat_col = st.columns([3, 1.2], gap="medium")
view: ws.WorkspaceView = st.session_state.view

with main_col:

    # ---- TABLE ----
    st.markdown(f'<div class="panel-label">Table — {view.title}</div>', unsafe_allow_html=True)
    if view.table is not None and not view.table.empty:
        st.dataframe(view.table, use_container_width=True, hide_index=True, height=480)
    else:
        st.dataframe(pd.DataFrame({"Info": ["No records to display."]}),
                     use_container_width=True, hide_index=True, height=480)

    # ---- STAT CARDS ----
    boxes_html = '<div class="scroll-row">'
    for b in view.info_boxes:
        boxes_html += (
            '<div class="info-box">'
            f'<div class="box-title">{b.title}</div>'
            f'<div class="big-stat">{b.stat}</div>'
            f'<div class="box-body">{b.body}</div>'
            "</div>"
        )
    boxes_html += "</div>"
    st.markdown(boxes_html, unsafe_allow_html=True)

    # ---- CHARTS (two per row) ----
    if view.charts:
        st.markdown('<div class="charts-label">Visual Analytics</div>', unsafe_allow_html=True)
        for i in range(0, len(view.charts), 2):
            pair = view.charts[i:i + 2]
            cols = st.columns(len(pair))
            for col, chart in zip(cols, pair):
                with col:
                    st.caption(chart.title)
                    st.plotly_chart(chart.figure, use_container_width=True)

with chat_col:
    st.markdown('<div class="panel-label">Chat Box</div>', unsafe_allow_html=True)
    with st.container(height=430, border=True):
        if not st.session_state.messages:
            st.caption("Ask the assistant something…")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    prompt = st.chat_input("Text here")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            with st.spinner("Working…"):
                new_view, reply = ws.route_message(prompt)
            if new_view is not None:
                st.session_state.view = new_view
        except requests.exceptions.ConnectionError:
            reply = ("I couldn't reach the API. Start it with "
                     "`uvicorn app.main:app --reload` and check BASE_URL in your .env.")
        except Exception as e:  # noqa: BLE001
            reply = f"Something went wrong: `{e}`"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()