from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import asc, select

from . import models, schemas
import asyncio


async def get_all_medications(db: AsyncSession):
    result = await db.execute(
        select(models.Medication)
        .options(selectinload(models.Medication.prescriptions))
        .order_by(asc(models.Medication.id))
    )
    return result.scalars().all()


async def get_all_patients(db: AsyncSession):
    result = await db.execute(
        select(models.Patient)
        .options(selectinload(models.Patient.prescriptions))
        .order_by(models.Patient.id)
    )
    return result.scalars().all()


async def get_all_prescriptions(db: AsyncSession):
    result = await db.execute(
        select(models.Prescription)
        .options(selectinload(models.Prescription.medication),
                 selectinload(models.Prescription.patient))
        .order_by(models.Prescription.id)
    )
    return result.scalars().all()


async def get_medication(db: AsyncSession, medication_id: int):
    result = await db.execute(
        select(models.Medication)
        .options(selectinload(models.Medication.prescriptions))
        .where(models.Medication.id == medication_id)
    )
    res = result.scalar_one_or_none()
    if res is None:
        raise HTTPException(status_code=404, detail=f"medication with id {medication_id} not found")
    return res

async def get_patient(db: AsyncSession, patient_id: int):
    result = await db.execute(
        select(models.Patient)
        .options(selectinload(models.Patient.prescriptions))
        .where(models.Patient.id == patient_id)
    )
    res = result.scalar_one_or_none()
    if res is None:
        raise HTTPException(status_code=404, detail=f"patient with id {patient_id} not found")
    return res


async def get_prescription(db: AsyncSession, prescription_id: int):
    result = await db.execute(
        select(models.Prescription)
        .options(selectinload(models.Prescription.medication), 
                 selectinload(models.Prescription.patient))
        .where(models.Prescription.id == prescription_id)
    )
    res = result.scalar_one_or_none()
    if res is None:
        raise HTTPException(status_code=404, detail=f"prescription with id {prescription_id} not found")
    return res


async def update_medication(db: AsyncSession, medication_id: int, medication: models.Medication):
    result = await db.execute(
        select(models.Medication)
        .options(selectinload(models.Medication.prescriptions))
        .where(models.Medication.id == medication_id)
    )
    res = result.scalar_one_or_none()
    if res is None:
        raise HTTPException(status_code=404, detail=f"medication with id {medication_id} not found")
    for key, value in medication.dict().items():
        setattr(res, key, value)
    db.add(res)
    await db.commit()
    await db.refresh(res)
    return res


async def update_patient(db: AsyncSession, patient_id: int, patient: models.Patient):
    result = await db.execute(
        select(models.Patient)
        .options(selectinload(models.Patient.prescriptions))
        .where(models.Patient.id == patient_id)
    )
    res = result.scalar_one_or_none()
    if res is None:
        raise HTTPException(status_code=404, detail=f"patient with id {patient_id} not found")
    for key, value in patient.dict().items():
        setattr(res, key, value)
    db.add(res)
    await db.commit()
    await db.refresh(res)
    return res


async def update_perscription(db: AsyncSession, prescription_id: int, prescription: models.Prescription):
    result = await db.execute(
        select(models.Prescription)
        .options(selectinload(models.Prescription.medication),
                 selectinload(models.Prescription.patient))
        .where(models.Prescription.id == prescription_id)
    )
    res = result.scalar_one_or_none()
    if res is None:
        raise HTTPException(status_code=404, detail=f"prescription with id {prescription_id} not found")
    for key, value in prescription.dict().items():
        setattr(res, key, value)
    db.add(res)
    await db.commit()
    await db.refresh(res)
    return res


async def create_medication(db: AsyncSession, medication: schemas.MedicationCreate):
    db_model = models.Medication(**medication.model_dump())
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)

    db_model.prescriptions = []
    return db_model


async def create_patient(db: AsyncSession, patient: schemas.PatientCreate):
    db_model = models.Patient(**patient.model_dump())
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)

    db_model.prescriptions = []
    return db_model


async def create_prescription(db: AsyncSession, prescription: schemas.PrescriptionCreate):
    db_model = models.Prescription(**prescription.model_dump())
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)

    db_model.medication = []
    db_model.patient = []
    return db_model


async def delete_medication(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Medication)
        .options(selectinload(models.Medication.prescriptions))
        .where(models.Medication.id == id)
    )
    med = result.scalar_one_or_none()
    if med is None:
        raise HTTPException(status_code=404, detail=f"medication with id {id} not found")
    await db.delete(med)
    await db.commit()
    return med


async def delete_patient(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Patient)
        .options(selectinload(models.Patient.prescriptions))
        .where(models.Patient.id == id)
    )
    patient = result.scalar_one_or_none()
    if patient is None:
        raise HTTPException(status_code=404, detail=f"patient with id {id} not found")
    await db.delete(patient)
    await db.commit()
    return patient


async def delete_prescription(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Prescription)
        .options(selectinload(models.Prescription.medication),
                 selectinload(models.Prescription.patient))
        .where(models.Prescription.id == id)
    )
    prescription = result.scalar_one_or_none()
    if prescription is None:
        raise HTTPException(status_code=404, detail=f"prescription with id {id} not found")
    await db.delete(prescription)
    await db.commit()
    return prescription