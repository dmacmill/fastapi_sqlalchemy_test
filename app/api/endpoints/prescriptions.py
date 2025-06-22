from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app import crud, schemas
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get("/all_prescriptions", response_model=List[schemas.Prescription])
async def all_prescriptions(db: AsyncSession = Depends(get_db)):
    prescriptions = await crud.get_all_prescriptions(db)
    return prescriptions


@router.get("/prescription/{id}", response_model=schemas.Prescription)
async def get_prescription(id: int, 
                db: AsyncSession = Depends(get_db)):
    return await crud.get_prescription(db=db, prescription_id=id)


@router.post("/prescription", response_model=schemas.Prescription)
async def create_prescription(prescription: schemas.PrescriptionCreate, 
                   db: AsyncSession = Depends(get_db)):
    return await crud.create_prescription(db=db, prescription=prescription)


@router.patch("/prescription/{id}", response_model=schemas.Prescription)
async def update_prescription(id: int,
                   prescription: schemas.PrescriptionCreate,
                   db: AsyncSession = Depends(get_db)):
    return await crud.update_prescription(db=db, prescription_id=id, prescription=prescription)


@router.delete("/prescription/{id}", response_model=schemas.Prescription)
async def delete_prescription(id: int,
                   db: AsyncSession = Depends(get_db)):
    return await crud.delete_prescription(db, id)
