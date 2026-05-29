import asyncio
import json

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    SystemMessage,
    AIMessage,
)

from app.llm.mcp_client import get_tools


# ==========================================
# SYSTEM PROMPT (compressed — Fix B)
# ==========================================
SYSTEM_PROMPT = """
You are a workspace-oriented AI assistant for a Plant Downtime Management System.
You manage machines, maintenance logs, downtime events, and downtime causes via MCP tools.

RULES:
1. Always use a tool when database data is needed. Never invent IDs, records, or tool names.
2. To act on a record by name or for a specific machine, use the find_* tools
   (e.g. find_machines_by_name, find_maintenance_by_machine). For OPEN-ENDED
   questions or summaries (e.g. "what are the trends", "tell me about X"),
   call get_all_* ONCE and answer from that — never call find_* with an empty
   or wildcard argument.
3. If a name or filter matches multiple records, list the matches with their IDs and ask
   the user to resend the command using the specific ID. Never guess.
4. When updating, only change fields the user explicitly mentioned.
5. After a successful action, the workspace refreshes automatically — just give a SHORT
   confirmation in chat (e.g. "Machine added.", "Loaded maintenance logs.").
6. Never dump records, JSON, or tables into chat. The workspace shows that. Keep replies brief.
7. Dates: YYYY-MM-DD. Datetimes: YYYY-MM-DDTHH:MM:SS.
8. After you receive tool results, respond with a SHORT final text message. Do NOT call the
   same tool again if you already have its result.
9. For analytical or "trend" questions (e.g. "what are the trends",
   "any patterns", "anything notable"), do NOT just describe what columns
   or values exist. Identify concrete patterns: imbalances, outliers,
   skewed distributions, dominant categories, gaps, or notable concentrations.
   Use specific numbers (counts, percentages, ratios) from the data — not
   vague phrases like "various" or "mostly". If nothing notable stands out,
   say so honestly.
"""


# ==========================================
# HISTORY TRIMMING (Fix A)
# ==========================================
def _trim_messages(messages, keep_last: int = 10):
    """
    Keep the system prompt + the most recent messages, so old tool-result
    dumps are not re-sent every iteration.

    The tool protocol requires every ToolMessage to be preceded by the
    AIMessage that requested it, so if the window would start on a ToolMessage
    we step back to include its owning AIMessage.
    """
    if len(messages) <= keep_last + 1:
        return messages
    system = messages[0]
    start_index = len(messages) - keep_last
    while start_index > 1 and isinstance(messages[start_index], ToolMessage):
        start_index -= 1
    return [system] + messages[start_index:]


# ==========================================
# MAIN AGENT
# ==========================================
MAX_STEPS = 6   # Fix D — cap reasoning/tool cycles


async def run_agent_async(user_query: str):

    tools_called: list[str] = []

    tools = await get_tools()

    named_tools = {tool.name: tool for tool in tools}

    # llm = ChatGroq(

    #     model="llama-3.3-70b-versatile",

    #     temperature=0
    # )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_query),
    ]

    for _ in range(MAX_STEPS):

        response = await llm_with_tools.ainvoke(_trim_messages(messages))
        messages.append(response)

        print("\nRAW MODEL MESSAGE:\n")
        print(response)

        # No more tool calls -> final answer
        if not response.tool_calls:
            return {"reply": response.content, "tools_called": tools_called}

        # Execute each requested tool
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})
            tool_id = tool_call["id"]

            tools_called.append(tool_name)

            print("\nTOOL NAME:\n", tool_name)
            print("\nTOOL ARGS:\n", tool_args)

            selected_tool = named_tools[tool_name]
            result = await selected_tool.ainvoke(tool_args)

            print("\nTOOL RESULT:\n", result)

            messages.append(
                ToolMessage(
                    tool_call_id=tool_id,
                    content=json.dumps(result),
                )
            )

    return {
        "reply": "I couldn't fully complete that within the step limit. "
                 "Please check the result or try rephrasing.",
        "tools_called": tools_called,
    }


# ==========================================
# STREAMLIT WRAPPER
# ==========================================
def run_agent(user_query: str) -> dict:
    """Returns {"reply": str, "tools_called": list[str]}."""
    return asyncio.run(run_agent_async(user_query))