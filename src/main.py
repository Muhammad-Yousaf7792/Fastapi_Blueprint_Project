from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from .api.db.session import init_db
from .api.events import router as event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except RuntimeError as exc:
        print(f"Skipping DB init: {exc}")
    yield
    


app = FastAPI(lifespan=lifespan)
app.include_router(event_router, prefix='/api/events')



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_items():
    return {"items": []}


@app.get("/items/")
def read_items_slash():
    return {"items": ["Rana Yousaf"]}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}