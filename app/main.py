from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat
from app.routes import (
    machines,
    downtime_events,
    downtime_causes,
    maintenance_logs
)

app = FastAPI()

app.include_router(machines.router)

app.include_router(downtime_events.router)

app.include_router(downtime_causes.router)

app.include_router(maintenance_logs.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)