from fastapi import APIRouter, Depends, HTTPException

from app import crud, schemas
from app.db import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/all_perscriptions")
def all_perscriptions(db: Session = Depends(get_db)):
    perscriptions = crud.get_all_perscriptions(db)
    return perscriptions


@router.get("/perscription/{id}", response_model=schemas.Perscription)
def get_perscription(id: int, 
                db: Session = Depends(get_db)):
    return crud.get_perscription(db=db, perscription_id=id)


@router.post("/perscription", response_model=schemas.Perscription)
def create_perscription(perscription: schemas.PerscriptionCreate, 
                   db: Session = Depends(get_db)):
    return crud.create_perscription(db=db, perscription=perscription)


@router.patch("/perscription/{id}", response_model=schemas.Perscription)
def update_perscription(id: int,
                   perscription: schemas.PerscriptionCreate,
                   db: Session = Depends(get_db)):
    return crud.update_perscription(db=db, perscription_id=id, perscription=perscription)


@router.delete("/perscription/{id}", response_model=schemas.Perscription)
def delete_perscription(id: int,
                   db: Session = Depends(get_db)):
    return crud.delete_perscription(db, id)