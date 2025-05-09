from fastapi import APIRouter, Depends, HTTPException

from app import crud, schemas
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/all_patients")
async def all_patients(db: AsyncSession = Depends(get_db)):
    patients = await crud.get_all_patients(db)
    return patients


@router.get("/patient/{id}", response_model=schemas.Patient)
async def get_patient(id: int, 
                      db: AsyncSession = Depends(get_db)):
    return await crud.get_patient(db=db, patient_id=id)


@router.post("/patient", response_model=schemas.Patient)
async def create_patient(patient: schemas.PatientCreate, 
                         db: AsyncSession = Depends(get_db)):
    return await crud.create_patient(db=db, patient=patient)


@router.patch("/patient/{id}", response_model=schemas.Patient)
async def update_patient(id: int,
                         patient: schemas.PatientCreate,
                         db: AsyncSession = Depends(get_db)):
    return await crud.update_patient(db=db, patient_id=id, patient=patient)


@router.delete("/patient/{id}", response_model=schemas.Patient)
async def delete_patient(id: int,
                         db: AsyncSession = Depends(get_db)):
    return await crud.delete_patient(db, id)