from sqlalchemy import create_engine, engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings


# Create the SQLAlchemy engine and adding a database URL in it
# connect_args is needed only for SQLite. It's not needed for other databases
engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
