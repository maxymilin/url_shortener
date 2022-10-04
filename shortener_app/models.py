from itertools import count

from sqlalchemy import Column, Integer, String
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select


from .database import Base, db


class URL(Base):
    """Save to database target url and short code."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    calls_count = Column(Integer, default=1)

    @classmethod
    async def create(cls, key, target_url):
        db_url = cls(key=key, target_url=target_url)
        print(db_url)
        db.add(db_url)

        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        return db_url

    @classmethod
    async def get(cls, url):
        query = select(cls).where(cls.key == url)
        full_urls = await db.execute(query)
        try:
            (full_url,) = full_urls.first()
            return full_url
        except TypeError:
            return None

    @classmethod
    async def is_exist(cls, target_url):
        query = select(cls).where(cls.target_url == target_url)
        full_urls = await db.execute(query)
        try:
            (full_url,) = full_urls.first()
            return full_url
        except TypeError:
            return False

    @classmethod
    async def calls(cls):
        query = select(cls.count)
        num_calls = await db.execute(query)
        num_calls = sum(num_calls.scalars().all())

    @classmethod
    async def update_calls(cls, url, calls_count):
        query = (
            sqlalchemy_update(cls)
            .where(cls.target_url == url)
            .values(calls_count=calls_count)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
