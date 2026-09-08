from dataclasses import dataclass
import os


@dataclass
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/research_agent",
    )

settings = Settings()  