import secrets
import validators

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from . import models, schemas
from .database import async_session, Base, engine
from .models_dal import UrlDAL

app = FastAPI()


@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    massage = f"URL {request.url} doesn't exist."
    raise HTTPException(status_code=404, detail=massage)


@app.get("/")
async def root():
    return "Hello, World"


@app.post("/shorten_url", response_model=schemas.URL)
async def create_url(url: schemas.URLBase):
    async with async_session() as session:
        async with session.begin():
            if not validators.url(url.target_url):
                raise_bad_request(message="URL is not valid")
            print("I get url", url.target_url)
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            key = "".join(secrets.choice(chars) for _ in range(5))
            db_url = models.URL(
                target_url=url.target_url, key=key
            )
            url_dal = UrlDAL(session)
            await url_dal.create_url(db_url)
            db_url.url = key
            return db_url


# @app.get("/{url_key}")
# def forvard_to_target_url(
#     url_key: str, request: Request, db: Session = Depends(get_db)
# ):
#     db_url = (
#         db.query(models.URL).filter(models.URL.key == url_key).first()
#     )
#     if db_url:
#         return RedirectResponse(db_url.target_url)
#     else:
#         raise_not_found(request)
