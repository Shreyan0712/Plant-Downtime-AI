import json

from legacy.groq_client import (
    ask_groq
)

def parse_action(user_query):

    prompt = f"""
You are an AI API action parser.

Your job is to convert user requests
into structured JSON actions.

Allowed operations:
- get
- create
- update
- delete

Allowed entities:
- machines
- maintenance_logs
- downtime_events
- downtime_causes


Machines schema:

{{
    "machine_name": "string",
    "location": "string",
    "category": "string",
    "status": "string"
}}


Maintenance Logs schema:

{{
    "machine_id": "integer",
    "maintenance_type": "string",
    "technician": "string"
}}


Downtime Events schema:

{{
    "machine_id": "integer",
    "reason_category": "string"
}}


Downtime Causes schema:

{{
    "downtime_id": "integer",
    "root_cause": "string"
}}


RULES:
- Return ONLY valid JSON
- No explanation
- No markdown
- No extra text
- Infer reasonable missing fields if possible
- IDs must always be integers
- Never return IDs as strings
- Extract only numeric ID values


EXAMPLES:


User:
Delete machine 5

Output:

{{
    "operation": "delete",
    "entity": "machines",
    "id": 5
}}


User:
Show all maintenance logs

Output:

{{
    "operation": "get",
    "entity": "maintenance_logs"
}}


User:
Create a maintenance log for machine 3
with technician Rahul Sharma

Output:

{{
    "operation": "create",
    "entity": "maintenance_logs",
    "data": {{
        "machine_id": 3,
        "technician": "Rahul Sharma"
    }}
}}


User:
Update machine 2 status to Idle

Output:

{{
    "operation": "update",
    "entity": "machines",
    "id": 2,
    "data": {{
        "status": "Idle"
    }}
}}

User:
Delete machine id 27

Output:

{{
    "operation": "delete",
    "entity": "machines",
    "id": 27
}}


User:
Delete downtime cause 5

Output:

{{
    "operation": "delete",
    "entity": "downtime_causes",
    "id": 5
}}


USER QUERY:
{user_query}
"""

    response = ask_groq(prompt)

    return json.loads(response)