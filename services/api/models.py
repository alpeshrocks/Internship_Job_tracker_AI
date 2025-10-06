from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://tracker:tracker@db:5432/tracker")
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    job_uid = Column(String, unique=True, nullable=False, index=True)
    source = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String)
    employment_type = Column(String)
    remote_ok = Column(Boolean)
    visa_friendly = Column(Boolean)
    posted_date = Column(DateTime)
    scraped_at = Column(DateTime, server_default=func.now())
    link = Column(String, nullable=False)
    skills = Column(Text)
    description = Column(Text)

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, nullable=False, index=True)
    applied = Column(Boolean, server_default="false")
    saved = Column(Boolean, server_default="false")
    notes = Column(Text)
    cold_email_sent = Column(Boolean, server_default="false")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
