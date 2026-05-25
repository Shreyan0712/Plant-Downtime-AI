import asyncio
import json

from langchain_groq import ChatGroq

from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    SystemMessage
)

from app.llm.mcp_client import (
    get_tools
)



# SYSTEM PROMPT

SYSTEM_PROMPT = """
You are an industrial AI assistant for a Plant Downtime Management System.
You manage machines, maintenance logs, downtime events, and downtime causes
using the available tools.

RULES:
1. Always use a tool when database data is needed. Never invent IDs or records.
2. To act on a record by NAME, first fetch the relevant table, find the exact
   matching record, and use its real ID. If multiple records match, ask the user
   which one — do NOT guess.
3. For multi-step requests, complete one operation before starting the next.
4. When updating, only change fields the user specified.
5. Dates: YYYY-MM-DD. Datetimes: YYYY-MM-DDTHH:MM:SS.
6. Present records clearly as a short numbered list.
"""


# LARGER DETAILED SYSTEM PROMPT


# SYSTEM_PROMPT = """
# You are an intelligent industrial AI assistant for a Plant Downtime Management System.

# You help users interact with the industrial plant database using natural language.

# You have access to MCP tools for managing:

# - machines
# - maintenance logs
# - downtime events
# - downtime causes

# --------------------------------------------------
# AVAILABLE TOOLS
# --------------------------------------------------

# MACHINE TOOLS:

# 1. get_all_machines
# Retrieve all machine records from the machines table.

# 2. get_machine_by_id_tool
# Retrieve a specific machine record using machine ID.

# 3. add_machine
# Create a new machine record.

# 4. edit_machine
# Update an existing machine record.

# 5. remove_machine
# Delete a machine record.

# --------------------------------------------------

# MAINTENANCE LOG TOOLS:

# 6. get_all_maintenance_logs
# Retrieve all maintenance log records.

# 7. get_maintenance_log_by_id_tool
# Retrieve a specific maintenance log record.

# 8. add_maintenance_log
# Create a new maintenance log entry.

# 9. edit_maintenance_log
# Update an existing maintenance log.

# 10. remove_maintenance_log
# Delete a maintenance log.

# --------------------------------------------------

# DOWNTIME EVENT TOOLS:

# 11. get_all_downtime_events
# Retrieve all downtime event records.

# 12. get_downtime_event_by_id_tool
# Retrieve a downtime event using downtime ID.

# 13. add_downtime_event
# Create a new downtime event.

# 14. edit_downtime_event
# Update an existing downtime event.

# 15. remove_downtime_event
# Delete a downtime event.

# --------------------------------------------------

# DOWNTIME CAUSE TOOLS:

# 16. get_all_downtime_causes
# Retrieve all downtime cause records.

# 17. get_downtime_cause_by_id_tool
# Retrieve a downtime cause using cause ID.

# 18. add_downtime_cause
# Create a downtime cause record.

# 19. edit_downtime_cause
# Update a downtime cause record.

# 20. remove_downtime_cause
# Delete a downtime cause record.

# --------------------------------------------------
# GENERAL RULES
# --------------------------------------------------

# 1. Always use tools whenever database information is required.

# 2. Never invent tool names.

# 3. Never hallucinate records or database values.

# 4. Never generate fake IDs or fake records.

# 5. Never output raw JSON unless explicitly requested.

# 6. Always format records clearly and consistently.

# 7. Use numbered lists whenever multiple records are displayed.

# 8. If multiple operations are requested:
# - perform them sequentially
# - complete one operation before starting the next
# - use multiple tool calls if required

# 9. When updating records:
# - only update fields explicitly mentioned by the user

# 10. When datetime values are required, always use ISO format:

# YYYY-MM-DDTHH:MM:SS

# Example:
# 2025-01-30T10:00:00

# 11. When date values are required, use format:

# YYYY-MM-DD

# Example:
# 2025-05-22

# --------------------------------------------------
# RECORD DISPLAY FORMAT
# --------------------------------------------------

# When displaying records from ANY table:

# - Show EVERY available column for EACH record
# - Display records in a structured readable format
# - Never skip important fields
# - Use numbered formatting

# Example:

# 1.
# Record Details:
# field_name_1: value
# field_name_2: value
# field_name_3: value

# 2.
# Record Details:
# field_name_1: value
# field_name_2: value
# field_name_3: value

# --------------------------------------------------
# MACHINE RECORD DISPLAY
# --------------------------------------------------

# Always display ALL available machine fields including:

# - machine_id
# - machine_name
# - status
# - location
# - category
# - install_date

# Example:

# 1.
# Machine Details:
# Machine ID: 1
# Machine Name: Lathe Machine A
# Status: Running
# Location: Line 1
# Category: Lathe
# Install Date: 2020-01-10

# --------------------------------------------------
# MAINTENANCE LOG DISPLAY
# --------------------------------------------------

# Always display ALL available maintenance log fields including:

# - maintenance_id
# - machine_id
# - maintenance_type
# - start_time
# - end_time
# - work_done
# - technician

# --------------------------------------------------
# DOWNTIME EVENT DISPLAY
# --------------------------------------------------

# Always display ALL available downtime event fields including:

# - downtime_id
# - machine_id
# - reason_category
# - start_time
# - end_time

# --------------------------------------------------
# DOWNTIME CAUSE DISPLAY
# --------------------------------------------------

# Always display ALL available downtime cause fields including:

# - cause_id
# - downtime_id
# - root_cause


# """


# ==========================================
# MAIN AGENT
# ==========================================

async def run_agent_async(
    user_query: str
):

    # LOAD MCP TOOLS

    tools = await get_tools()

    # TOOL MAP

    named_tools = {}

    for tool in tools:

        named_tools[tool.name] = tool

    # CREATE LLM

    llm = ChatGroq(

        model="llama-3.3-70b-versatile",

        temperature=0
    )

    # BIND TOOLS

    llm_with_tools = llm.bind_tools(
        tools
    )

    # INITIAL CONVERSATION

    messages = [

        SystemMessage(
            content=SYSTEM_PROMPT
        ),

        HumanMessage(
            content=user_query
        )
    ]

    
    # ITERATIVE AGENT LOOP
    
    while True:

        # LLM REASONING STEP

        response = await llm_with_tools.ainvoke(
            messages
        )

        messages.append(response)

        print("\nRAW MODEL MESSAGE:\n")
        print(response)

        # FINAL RESPONSE (NO MORE TOOLS)
        
        if not response.tool_calls:

            return response.content

        # EXECUTE TOOL CALLS
        
        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call.get(
                "args",
                {}
            )

            tool_id = tool_call["id"]

            print("\nTOOL NAME:\n")
            print(tool_name)

            print("\nTOOL ARGS:\n")
            print(tool_args)

            # GET TOOL

            selected_tool = named_tools[
                tool_name
            ]

            # EXECUTE TOOL

            result = await selected_tool.ainvoke(
                tool_args
            )

            print("\nTOOL RESULT:\n")
            print(result)

            # ADD TOOL RESULT TO CONVERSATION

            messages.append(

                ToolMessage(

                    tool_call_id=tool_id,

                    content=json.dumps(result)
                )
            )


# STREAMLIT WRAPPER

def run_agent(
    user_query: str
):

    return asyncio.run(

        run_agent_async(
            user_query
        )
    )