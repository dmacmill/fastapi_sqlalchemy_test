from fastapi import APIRouter, Depends, HTTPException

from app import crud, schemas
from app.db import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/all_patients")
def all_patients(db: Session = Depends(get_db)):
    patients = crud.get_all_patients(db)
    return patients


@router.get("/patient/{id}", response_model=schemas.Patient)
def get_patient(id: int, 
                db: Session = Depends(get_db)):
    return crud.get_patient(db=db, patient_id=id)


@router.post("/patient", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, 
                   db: Session = Depends(get_db)):
    return crud.create_patient(db=db, patient=patient)


@router.patch("/patient/{id}", response_model=schemas.Patient)
def update_patient(id: int,
                   patient: schemas.PatientCreate,
                   db: Session = Depends(get_db)):
    return crud.update_patient(db=db, patient_id=id, patient=patient)


@router.delete("/patient/{id}", response_model=schemas.Patient)
def delete_patient(id: int,
                   db: Session = Depends(get_db)):
    return crud.delete_patient(db, id)