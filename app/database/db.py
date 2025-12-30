from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL =", DATABASE_URL)  # DEBUG

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set. Check .env file.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
