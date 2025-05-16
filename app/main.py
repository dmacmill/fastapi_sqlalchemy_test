import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
LOGGER = logging.getLogger(__name__)

from app.api.api import router
from app import models
from app.models import Medication, Patient, Prescription # needed for pytest to see
from app.db import engine


# create the database tables
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# define how the app's life will run. "await on_startup()" creates the tables in the db, yield runs things,
# and stuff after yield cleans things up 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # await on_startup()
    LOGGER.warning("lifespan starting!!!")
    yield # run
    LOGGER.warning("lifespan ending!!!!")
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.destroy_all)

description = """FastAPI with SQLAlchemy, aimed for small-scale projects and educational purposes."""
app = FastAPI(
    title="FastAPI with SQLAlchemy",
    description=description,
    version="0.1.0",
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', 'http://192.168.1.160:8000', "http://localhost:8000", "http://db:8000", "http://test"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router, prefix="/api")


# root path
@app.get("/")
def hello_world():
    message = f"Hello world!"
    return {"message": message}
