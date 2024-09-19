from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import logging
logging.basicConfig()    
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

from app.api.api import router
from app import models
from app.db import engine

models.Base.metadata.create_all(bind=engine)


description = """This API is the one with an ORM, it should do the same stuff 
that the other API does though, which is testing ideas I have."""
app = FastAPI(
    title="FastAPI with SQLAlchemy",
    description=description,
    version="0.0.1"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', 'http://192.168.1.160:8000', "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router, prefix="/api")

# our shit, TODO: move to app/app.py type thing
@app.get("/")
def hello_world():
    message = f"Hello world!"
    return {"message": message}
