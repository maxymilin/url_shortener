from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import get_settings


# Create the SQLAlchemy engine and adding a database URL in it
engine = create_async_engine(get_settings().db_url, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
