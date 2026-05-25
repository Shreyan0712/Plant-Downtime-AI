import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

#Server config

SERVERS = {
    "plant-downtime-server" : {
        "transport" : "stdio",

        "command" : "python",

        "args" : [
            
            "-m",
            "app.mcp_server"
        ]
    }
}

#MCP Client creation

client = MultiServerMCPClient(
    SERVERS
)

#Get Tools

async def get_tools():

    tools = await client.get_tools()

    return tools

#Execute Tools

async def execute_tool(
        tool,
        tool_args: dict
):
    
    result = await tool.ainvoke(
        tool_args
    )

    return result