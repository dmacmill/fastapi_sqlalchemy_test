from fastapi import APIRouter, Depends, HTTPException

from app import crud, schemas
from app.db import get_db
from sqlalchemy.orm import Session


router = APIRouter()


# TODO: async def via this tutorial: https://medium.com/@navinsharma9376319931/mastering-fastapi-crud-operations-with-async-sqlalchemy-and-postgresql-3189a28d06a2
@router.get("/all_medications")
def all_medications(db: Session = Depends(get_db)):
    # Notice that the values you return are SQLAlchemy models, or lists of SQLAlchemy models.
    #
    # But as all the path operations have a response_model with Pydantic models / schemas using orm_mode, the data declared 
    # in your Pydantic models will be extracted from them and returned to the client, with all the normal filtering and validation.
    meds = crud.get_all_medications(db)
    return meds


@router.post("/medication", response_model=schemas.Medication)
def create_medication(med: schemas.MedicationCreate,
                      db: Session = Depends(get_db)):
    return crud.create_medication(db=db, medication=med)


@router.patch("/medication", response_model=schemas.Medication)
def update_medication(id: int,
                      med: schemas.MedicationCreate,
                      db: Session = Depends(get_db)):
    return crud.update_medication(db, id, med)


@router.delete("/medication")
def delete_medication(id: int,
                      db: Session = Depends(get_db)):
    return crud.delete_medication(db, id)