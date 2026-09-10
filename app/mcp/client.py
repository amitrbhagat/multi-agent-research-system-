from contextlib import asynccontextmanager
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from app.config import settings



def get_search_server_params() -> StdioServerParameters:
    return StdioServerParameters(
        command=settings.mcp_search_command,
        args = settings.mcp_search_args,
        env = {"TAVILY_API_KEY": settings.tavily_api_key},
    )

@asynccontextmanager
async def mcp_search_session():
    params = get_search_server_params()
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session    



def get_fetch_server_params() -> StdioServerParameters:
    return StdioServerParameters(
        command=settings.mcp_fetch_command,
        args=settings.mcp_fetch_args,
        env={},
    )


@asynccontextmanager
async def mcp_fetch_session():
    """Opens an MCP session against the page-fetch server and yields it."""
    params = get_fetch_server_params()
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session
            