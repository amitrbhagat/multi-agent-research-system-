from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import settings




engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


def get_engine():
    return engine


def check_connection() -> bool:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return result.scalar() == 1


if __name__ == "__main__":
    print(check_connection())