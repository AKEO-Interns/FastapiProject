from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.appConfig import Settings

DATABASE_URL = Settings.DATABASE_URL

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set. Check .env file.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
