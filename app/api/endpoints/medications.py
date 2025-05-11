from fastapi import APIRouter, Depends, HTTPException

from app import crud, schemas
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/all_medications")
async def all_medications(db: AsyncSession = Depends(get_db)):
    # Notice that the values you return are SQLAlchemy models, or lists of SQLAlchemy models.
    #
    # But as all the path operations have a response_model with Pydantic models / schemas using orm_mode, the data declared 
    # in your Pydantic models will be extracted from them and returned to the client, with all the normal filtering and validation.
    meds = await crud.get_all_medications(db)
    return meds


@router.get("/medication/{id}", response_model=schemas.Medication)
async def get_medication(id: int, 
                         db: AsyncSession = Depends(get_db)):
    return await crud.get_medication(db=db, medication_id=id)


@router.post("/medication", response_model=schemas.Medication)
async def create_medication(med: schemas.MedicationCreate,
                            db: AsyncSession = Depends(get_db)):
    return await crud.create_medication(db=db, medication=med)


@router.patch("/medication/{id}", response_model=schemas.Medication)
async def update_medication(id: int,
                            med: schemas.MedicationCreate,
                            db: AsyncSession = Depends(get_db)):
    return await crud.update_medication(db, id, med)


@router.delete("/medication/{id}")
async def delete_medication(id: int,
                            db: AsyncSession = Depends(get_db)):
    return await crud.delete_medication(db, id)