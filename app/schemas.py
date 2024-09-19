from pydantic import BaseModel

from datetime import date

from typing import List, Optional


# TODO: separate these and add in /models dir
class MedicationBase(BaseModel):
    name: str
    use_case: str
    stock: int

    class Config:
        from_attributes = True


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


# Perscription
class PerscriptionBase(BaseModel):
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


class PerscriptionCreate(PerscriptionBase):
    pass


class Medication(MedicationBase):
    id: int
    perscriptions: list[PerscriptionBase] = []


class Patient(PatientBase):
    id: int
    perscriptions: list[PerscriptionBase] = []


class Perscription(PerscriptionBase):
    id: int
    medication: MedicationBase
    patient: PatientBase


Medication.model_rebuild()
Patient.model_rebuild()
