from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .env file lo nundi database URL teesukovadam
load_dotenv()

# Database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine create cheyadam (MySQL connection)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)

# Database session setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Database session get cheyadaniki function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()