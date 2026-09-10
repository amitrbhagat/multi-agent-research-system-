from dataclasses import dataclass, field
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/research_agent",
    )
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    mcp_search_command: str = os.getenv("MCP_SEARCH_SERVER_COMMAND", "npx")
    mcp_search_args: list[str] = field(
        default_factory=lambda: os.getenv(
            "MCP_SEARCH_SERVER_ARGS", "-y,tavily-mcp"
        ).split(",")
    )

settings = Settings()  
