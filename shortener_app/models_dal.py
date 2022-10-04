import secrets


from sqlalchemy.future import select
from sqlalchemy.orm import Session

from .models import URL


class UrlDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session


    async def create_url(self, target_url: str):
        print(target_url)
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        key = "".join(secrets.choice(chars) for _ in range(5))
        new_url = URL(key=key, target_url=target_url)
        print(new_url)
        self.db_session.add(new_url)
        await self.db_session.flush()
        return new_url


    async def get_url(self, key):
        q = await self.db_session.execute(select(URL).where(URL.key == key))
        print(q)
        target_url = q.scalars().first().target_url
        return target_url

