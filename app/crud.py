from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import asc

from . import models, schemas


def get_all_medications(db: Session):
    return db.query(models.Medication).order_by(models.Medication.id, asc(models.Medication.id)).all()


def get_all_patients(db: Session):
    return db.query(models.Patient).order_by(models.Patient.id, asc(models.Patient.id)).all()


def get_all_perscriptions(db: Session):
    return db.query(models.Perscription).order_by(models.Perscription.id, asc(models.Perscription.id)).all()


def get_medication(db: Session, medication_id: int):
    res = db.query(models.Medication).filter(models.Medication.id == medication_id).first()
    if res is None:
        raise HTTPException(status_code=404, detail="medication with id {} not found".format(medication_id))
    return res

def get_patient(db: Session, patient_id: int):
    res =  db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if res is None:
        raise HTTPException(status_code=404, detail="patient with id {} not found".format(patient_id))
    return res

def get_perscription(db: Session, perscription_id: int):
    res = db.query(models.Perscription).filter(models.Perscription.id == perscription_id).first()
    if res is None:
        raise HTTPException(status_code=404, detail="perscription with id {} not found".format(perscription_id))
    return res


def update_medication(db: Session, medication_id: int, medication: models.Medication):
    res = db.query(models.Medication).filter(models.Medication.id == medication_id).first()
    if res is None:
        raise HTTPException(status_code=404, detail="medication with id {} not found".format(medication_id))
    res.update(dict(
        name=medication.name,
        use_case=medication.use_case,
        stock=medication.stock
    ))
    db.commit()
    return res
    

def update_patient(db: Session, patient_id: int, patient: models.Patient):
    res = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if res is None:
        raise HTTPException(status_code=404, detail="patient with id {} not found".format(patient_id))
    res.update(dict(
        name=patient.name,
        phone_num=patient.phone_num,
        email=patient.email,
        insurance_num=patient.insurance_num,
        insurance_type=patient.insurance_type
    ))
    db.commit()
    return res


def update_perscription(db: Session, perscription_id: int, perscription: models.Perscription):
    res = db.query(models.Perscription).filter(models.Perscription.id == perscription_id).first()
    if res is None:
        raise HTTPException(status_code=404, detail="perscription with id {} not found".format(perscription_id))
    res.update(dict(
        medication_id=perscription.medication_id,
        patient_id=perscription.patient_id,
        dose=perscription.dose,
        every=perscription.every,
        amount=perscription.amount,
        refills=perscription.refills,
        last_filled=perscription.last_filled,
        day_supply=perscription.day_supply,
        doctor_name=perscription.doctor_name,
    ))
    db.commit()
    return res


def create_medication(db: Session, medication: models.Medication):
    db_med = models.Medication(
        name=medication.name,
        use_case=medication.use_case,
        stock=medication.stock
    )
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med


def create_patient(db: Session, patient: models.Patient):
    db_patient = models.Patient(
        name=patient.name,
        phone_num=patient.phone_num,
        email=patient.email,
        insurance_num=patient.insurance_num,
        insurance_type=patient.insurance_type
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def create_perscription(db: Session, perscription: models.Perscription):
    db_per = models.Perscription(
        medication_id=perscription.medication_id,
        patient_id=perscription.patient_id,
        dose=perscription.dose,
        every=perscription.every,
        amount=perscription.amount,
        refills=perscription.refills,
        last_filled=perscription.last_filled,
        day_supply=perscription.day_supply,
        doctor_name=perscription.doctor_name
    )
    db.add(db_per)
    db.commit()
    db.refresh(db_per)
    return db_per


def delete_medication(db: Session, id: int):
    med = db.query(models.Medication).filter(models.Medication.id == id).first()
    if med is None:
        raise HTTPException(status_code=404, detail="medication with id {} not found".format(id))
    db.delete(med)
    db.commit()
    return med


def delete_patient(db: Session, id: int):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="paitent with id {} not found".format(id))
    db.delete(patient)
    db.commit()
    return patient


def delete_perscription(db: Session, id: int):
    perscription = db.query(models.Perscription).filter(models.Perscription.id == id).first()
    if perscription is None:
        raise HTTPException(status_code=404, detail="perscription with id {} not found".format(id))
    db.delete(perscription)
    db.commit()
    return perscription