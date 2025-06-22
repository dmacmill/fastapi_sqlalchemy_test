from pydantic import BaseModel

from datetime import date

from typing import List, Optional


# TODO: separate these and add in /models dir
class MedicationBase(BaseModel):
    name: str
    use_case: str
    stock: int

    class Config:
        from_attributes = True  # once was "orm_mode = True"


class MedicationCreate(MedicationBase):
    pass


class PatientBase(BaseModel):
    name: str
    phone_num: str
    email: str
    insurance_num: str
    insurance_type: str

    class Config:
        from_attributes = True


class PatientCreate(PatientBase):
    pass


# Prescription
class PrescriptionBase(BaseModel):
    medication_id: int
    patient_id: int
    dose: str
    every: str
    amount: int
    refills: int
    last_filled: Optional[date]
    day_supply: int
    doctor_name: Optional[str]

    class Config:
        from_attributes = True


class PrescriptionCreate(PrescriptionBase):
    pass


class Medication(MedicationBase):
    id: int
    prescriptions: list[PrescriptionBase] = []

    class Config:
        from_attributes = True


class Patient(PatientBase):
    id: int
    prescriptions: list[PrescriptionBase] = []

    class Config:
        from_attributes = True


class Prescription(PrescriptionBase):
    id: int
    medication: MedicationBase
    patient: PatientBase

    class Config:
        from_attributes = True


Medication.model_rebuild()
Patient.model_rebuild()
