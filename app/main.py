from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from .api.v1 import router as router_v1
from .api.v1.user.auth import router as router_auth

from core.database import global_init


@asynccontextmanager
async def lifespan(app: FastAPI):
    await global_init()
    yield


app = FastAPI(title='Basic CRUD', version='0.0.1', lifespan=lifespan)
app.include_router(router_v1)
app.include_router(router_auth)


@app.get('/')
async def index():
    return {'Ping': 'Pong'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)