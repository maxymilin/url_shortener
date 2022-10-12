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


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
async def root():
    return {"message": "Hello, World"}


@app.get("/count")
async def get_url_count():
    count = await models.URL.calls()
    return {"message": f"Number of shortened urls: {count}"}


@app.get("/top10")
async def get_top_ten():
    result = await models.URL.get_top()
    return {"top_10_url": result}


async def get_client(url, client_ip):
    client = await models.Client.is_exist(client_ip, url.target_url)
    if client:
        return client
    return None


async def get_key(lenght=5):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    key = "".join(secrets.choice(chars) for _ in range(lenght))
    return key


async def get_url(url, request):
    client_ip = request.client.host
    exist_client = await get_client(client_ip, url)
    if exist_client:
        db_url_id = exist_client.url_id
        db_url = await models.URL.get(db_url_id)
    else:
        key = await get_key()
        db_url = await models.Client.create(
            client_ip=client_ip,
            target_url=url.target_url,
            key=key,
        )
    return db_url


@app.post("/shorten_url", response_model=schemas.URL)
async def create_url(url: schemas.URLBase, request: Request):
    if not validators.url(url.target_url):
        raise_bad_request(message="URL is not valid")
    db_url = await get_url(url, request)
    return db_url


@app.get("/{url_key}")
async def forvard_target_url(url_key: str, request: Request):
    db_url = await models.URL.get(key=url_key)
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
