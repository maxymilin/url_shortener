import secrets
import validators

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse


from .database import db
from . import models, schemas


db.init()

app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.create_all()


@app.on_event("shutdown")
async def shutdown():
    await db.close()


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
    if not validators.url(url.target_url):
        raise_bad_request(message="URL is not valid")
    exist_url = await models.URL.is_exist(url.target_url)
    if exist_url:
        update_calls = exist_url.calls_count + 1
        await models.URL.update_calls(url=url.target_url, calls_count=update_calls)
        return exist_url

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    key = "".join(secrets.choice(chars) for _ in range(5))
    db_url = await models.URL.create(target_url=url.target_url, key=key)
    return db_url


@app.get("/count")
async def get_url_count():
    count = await models.URL.calls()
    return f"Number of shortened urls: {count}"


@app.get("/{url_key}")
async def forvard_target_url(url_key: str, request: Request):
    db_url = await models.URL.get(url_key)
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
