import secrets
import validators

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
async def root():
    return "Hello, World"


@app.post("/shorten_url", response_model=schemas.URL)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    key = "".join(secrets.choice(chars) for _ in range(5))
    db_url = models.URL(target_url=url.target_url, key=key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key

    return db_url
