from sqlalchemy import Column, Integer, String
from sqlalchemy.future import select


from .database import Base, db


class URL(Base):
    """Save to database target url and short code."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)

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
