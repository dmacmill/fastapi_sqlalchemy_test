from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

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



@app.get("/all_medications")
def all_medications():
    # Notice that the values you return are SQLAlchemy models, or lists of SQLAlchemy models.
    #
    # But as all the path operations have a response_model with Pydantic models / schemas using orm_mode, the data declared 
    # in your Pydantic models will be extracted from them and returned to the client, with all the normal filtering and validation.
    meds = crud.get_all_medications()
    return meds


## Their shit
# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items