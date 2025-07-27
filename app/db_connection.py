from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DEV_DB_URL = getenv("DEV_DB_URL")

engine = create_engine(DEV_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
