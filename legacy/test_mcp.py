import asyncio

from app.llm.mcp_client import (
    get_tools
)


async def main():

    tools = await get_tools()

    tool_map = {}

    for tool in tools:

        tool_map[tool.name] = tool

    machine_tool = tool_map[
        "get_all_machines"
    ]

    result = await machine_tool.ainvoke({})

    print("\nTOOL RESULT:\n")

    print(result)


asyncio.run(main())