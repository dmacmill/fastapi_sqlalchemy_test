from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import logging
logging.basicConfig()    
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


from . import crud, models, schemas
from .db import SessionLocal, engine

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# our shit, TODO: move to app/app.py type thing
@app.get("/")
def hello_world():
    message = f"Hello world!"
    return {"message": message}


# Notice there is no "async def", this is because SQLAlchemy is too stupid for this.
@app.get("/all_medications")
def all_medications():
    # Notice that the values you return are SQLAlchemy models, or lists of SQLAlchemy models.
    #
    # But as all the path operations have a response_model with Pydantic models / schemas using orm_mode, the data declared 
    # in your Pydantic models will be extracted from them and returned to the client, with all the normal filtering and validation.
    meds = crud.get_all_medications()
    return meds
