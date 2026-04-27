import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

load_dotenv()
Database_URL = os.getenv("DATABASE_URL")

engine = create_engine(Database_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_session():
    """Get a new database session."""
    return SessionLocal()