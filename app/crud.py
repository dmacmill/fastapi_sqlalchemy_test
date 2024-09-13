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
    

def update_patient(db: Session, patient_id: int, patient: models.Patient):
    res = db.query(models.patient).filter(models.patient.id == patient_id).first()
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
    res = db.query(models.perscription).filter(models.perscription.id == perscription_id).first()
    res.update(dict(
        name=perscription.name,
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
        use_case=patient.use_case,
        stock=patient.stock
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def create_perscription(db: Session, perscription: models.Perscription):
    db_per = models.Perscription(
        name=perscription.name,
        use_case=perscription.use_case,
        stock=perscription.stock
    )
    db.add(db_per)
    db.commit()
    db.refresh(db_per)
    return db_per