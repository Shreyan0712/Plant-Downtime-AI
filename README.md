# AI-Powered Plant Downtime Data Management System

An AI-powered conversational database management system for industrial downtime data using:

- FastAPI
- SQLAlchemy
- MCP (Model Context Protocol)
- LangChain Agents
- Streamlit
- Angular

---

# Project Overview

This project allows users to interact with industrial downtime-related database records using natural language.

The system supports conversational CRUD operations for:

- Machines
- Maintenance Logs
- Downtime Events
- Downtime Causes

The AI system dynamically selects and executes tools using MCP and LangChain agent.

---

# Features

## Backend
- FastAPI REST APIs
- SQLAlchemy ORM
- CRUD operations
- Relational database design

## AI System
- MCP-based tool orchestration
- LangChain agent integration
- Dynamic tool calling


## Frontend
- Streamlit AI chat interface
- Planned AI workspace UI
- CRUD forms

---

# Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- Pydantic

## AI Systems
- LangChain
- MCP
- FastMCP
- LangChain MCP Adapters
- Groq LLM

## Frontend
- Streamlit
- Angular

---

# Database Tables

## Machines
- machine_id
- machine_name
- status
- location
- category
- install_date

## Maintenance Logs
- maintenance_id
- machine_id
- maintenance_type
- technician
- work_done
- start_time
- end_time

## Downtime Events
- downtime_id
- machine_id
- reason_category
- start_time
- end_time

## Downtime Causes
- cause_id
- downtime_id
- root_cause

---

# Project Architecture

User
↓
Streamlit Frontend
↓
LangChain Agent
↔
Groq LLM
↓
MCP Client
↓
FastMCP Server
↓
API Tools
↓
FastAPI Routes
↓
CRUD Layer
↓
SQLAlchemy ORM
↓
Database

---

# MCP Integration

The project uses FastMCP to expose backend functionalities as AI-usable tools.

Example MCP tools:

- get_all_machines
- add_machine
- edit_machine
- remove_machine

- get_all_maintenance_logs
- add_maintenance_log
- edit_maintenance_log
- remove_maintenance_log

---

# LangChain Agent Workflow

The LangChain agent follows an iterative reasoning loop:

1. User sends query
2. LLM reasons about intent
3. Appropriate tool is selected
4. MCP tool executes
5. Result is returned
6. LLM generates final response

This enables:
- dynamic tool selection
- multi-step workflows
- conversational database operations

---

# Folder Structure

```
Plant_Downtime_API/
│
├── app/                        # Backend (FastAPI + MCP + LLM agent)
│   ├── crud/                   # Database operations per table
│   ├── routes/                 # FastAPI REST endpoints per table
│   ├── schemas/                # Pydantic request/response models
│   ├── models/                 # SQLAlchemy ORM models
│   ├── llm/                    # AI layer
│   │   ├── agent.py            # LangChain agent (iterative tool-calling loop)
│   │   ├── api_tools.py        # REST API wrappers 
│   │   └── mcp_client.py       # MCP client (connects to the MCP server)
│   ├── legacy/                 # Pre-MCP experiments (manual tool routing)
│   ├── database.py             # DB connection / session
│   ├── main.py                 # FastAPI app entry point
│   └── mcp_server.py           # MCP server exposing backend tools
│
├── frontend/                   # Streamlit UI
│   ├── streamlit_app.py        # UI layout + page routing (run this)
│   ├── workspace.py            # Data layer: API calls, views, chat router
│   └── crud_forms.py           # Add / Update / Delete form pages
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example                # Template (no secrets) 
└── .env                        # Secrets (gitignored)
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repo-url>
cd Plant_Downtime_API
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows
```bash
venv\Scripts\activate
```

### Linux / Mac
```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Add Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_api_key
```

---

## 5. Run FastAPI Backend

```bash
uvicorn app.main:app --reload
```

---

## 6. Run Streamlit Frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

## 7. Run Angular Frontend

```bash
ng.serve
```

---

# Learning Outcomes

This project explored:

- Agentic AI systems
- MCP architecture
- LangChain agents
- Tool orchestration
- ReAct workflows
- Conversational AI
- Full-stack AI integration

---

# Author

Shreyan Dhar
