from fastapi import FastAPI
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