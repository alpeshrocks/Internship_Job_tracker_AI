import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL=os.getenv("DATABASE_URL","postgresql+psycopg://tracker:tracker@db:5432/tracker")
engine=create_engine(DATABASE_URL, future=True)
SessionLocal=sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
