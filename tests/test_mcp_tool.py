import asyncio

from app.mcp.client import mcp_search_session


async def main():
    async with mcp_search_session() as session:
        print("MCP connection established!")

        tools = await session.list_tools()

        print("Available MCP tools:")

        for tool in tools.tools:
            print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())