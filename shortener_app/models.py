from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
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
    async def get(cls, url_id):
        query = select(cls).where(cls.id == url_id)
        full_urls = await db.execute(query)
        try:
            (full_url,) = full_urls.first()
            return full_url
        except TypeError:
            return None

    @classmethod
    async def get_full_url(cls, url):
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
        query = select(cls.calls_count)
        num_calls = await db.execute(query)
        num_calls = sum(num_calls.scalars().all())
        return num_calls

    @classmethod
    async def update_calls(cls, url_id, calls):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == url_id)
            .values(calls_count=calls)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e

    @classmethod
    async def get_top(cls, limit=10):
        query = select(cls.target_url).order_by(cls.calls_count).limit(limit)
        top_result = await db.execute(query)
        top_result = top_result.scalars().all()
        return top_result


class Client(Base):
    """Table with unic URLs and count calls"""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    client_ip_url = Column(String, unique=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))

    @classmethod
    async def create(cls, client_ip, target_url, key):
        client_ip_url = client_ip + target_url
        db_url = await URL.is_exist(target_url)
        if db_url:
            url_id = db_url.id
            print("There are url", db_url.target_url)
            calls = db_url.calls_count + 1
            await db_url.update_calls(url_id, calls)
        else:
            db_url = await URL.create(target_url=target_url, key=key)
        db_client = cls(client_ip_url=client_ip_url, url_id=db_url.id)
        db.add(db_client)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        return db_url

    @classmethod
    async def is_exist(cls, client_ip, target_url):
        query = select(cls).where(cls.client_ip_url == client_ip + target_url)
        db_client = await db.execute(query)
        try:
            (full_url,) = db_client.first()
            return full_url
        except TypeError:
            return False
