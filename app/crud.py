from sqlalchemy.orm import Session

from . import models, schemas


def get_all_medications(db: Session):
    return db.query(models.Medication).all()


def get_all_patients(db: Session):
    return db.query(models.Patient).all()


def get_all_perscriptions(db: Session):
    return db.query(models.Perscription).all()


def get_medication(db: Session, medication_id: int):
    return db.query(models.Medication).filter(models.Medication.id == medication_id).first()


def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def get_perscription(db: Session, perscription_id: int):
    return db.query(models.Perscription).filter(models.Perscription.id == perscription_id).first()


def update_medication(db: Session, medication_id: int, medication: models.Medication):
    res = db.query(models.Medication).filter(models.Medication.id == medication_id).first()
    res.update(dict(
        name=medication.name,
        use_case=medication.use_case,
        stock=medication.stock
    ))
    db.commit()
    return res
    
