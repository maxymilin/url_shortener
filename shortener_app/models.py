from sqlalchemy import Column, Integer, String


from .database import Base


class URL(Base):
    """Save to database target url and short code."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
