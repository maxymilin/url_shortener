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


def raise_not_found(request):
    massage = f"URL {request.url} doesn't exist."
    raise HTTPException(status_code=404, detail=massage)


@app.get("/")
async def root():
    return "Hello, World"


@app.post("/shorten_url", response_model=schemas.URL)
async def create_url(url: schemas.URLBase, request: Request):
    client_ip = request.client.host + "|" #+ str(request.client.port) + "|"
    if not validators.url(url.target_url):
        raise_bad_request(message="URL is not valid")
    exist_client = await models.Client.is_exist(client_ip, url.target_url)
    if exist_client:
        db_url_id = exist_client.url_id
        db_url = await models.URL.get(db_url_id)
        key = db_url.key
    else:
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        key = "".join(secrets.choice(chars) for _ in range(5))
        db_url = await models.Client.create(
            client_ip=client_ip,
            target_url=url.target_url,
            key=key,
        )
    return db_url


@app.get("/count")
async def get_url_count():
    count = await models.URL.calls()
    return f"Number of shortened urls: {count}"


@app.get("/top10")
async def get_top_ten():
    result = await models.URL.get_top()
    return result


@app.get("/{url_key}")
async def forvard_target_url(url_key: str, request: Request):
    db_url = await models.URL.get(key=url_key)
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
