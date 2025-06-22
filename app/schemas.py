from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# ---------- Base Models ----------
class MedicationBase(BaseModel):
    name: str
    use_case: str
    stock: int

    class Config:
        from_attributes = True

class PatientBase(BaseModel):
    name: str
    phone_num: str
    email: str
    insurance_num: str
    insurance_type: str

    class Config:
        from_attributes = True

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

# ---------- Create Models ----------
class MedicationCreate(MedicationBase):
    pass

class PatientCreate(PatientBase):
    pass

class PrescriptionCreate(PrescriptionBase):
    pass


# ---------- Full Models with prescriptions list (for /medication and /patient endpoints) ----------

class PrescriptionSummary(PrescriptionBase):
    id: int

    class Config:
        from_attributes = True

class Medication(MedicationBase):
    id: int
    prescriptions: List[PrescriptionSummary] = []

    class Config:
        from_attributes = True

class Patient(PatientBase):
    id: int
    prescriptions: List[PrescriptionSummary] = []

    class Config:
        from_attributes = True


# ---------- Slimmed Models without prescriptions list (for /prescription endpoint) ----------

class MedicationSlim(MedicationBase):
    id: int

    class Config:
        from_attributes = True

class PatientSlim(PatientBase):
    id: int

    class Config:
        from_attributes = True

class Prescription(PrescriptionBase):
    id: int
    medication: MedicationSlim
    patient: PatientSlim

    class Config:
        from_attributes = True



# from pydantic import BaseModel

# from datetime import date

# from typing import List, Optional


# # TODO: separate these and add in /models dir
# class MedicationBase(BaseModel):
#     name: str
#     use_case: str
#     stock: int

#     class Config:
#         from_attributes = True  # once was "orm_mode = True"


# class MedicationCreate(MedicationBase):
#     pass


# class PatientBase(BaseModel):
#     name: str
#     phone_num: str
#     email: str
#     insurance_num: str
#     insurance_type: str

#     class Config:
#         from_attributes = True


# class PatientCreate(PatientBase):
#     pass


# # Prescription
# class PrescriptionBase(BaseModel):
#     medication_id: int
#     patient_id: int
#     dose: str
#     every: str
#     amount: int
#     refills: int
#     last_filled: Optional[date]
#     day_supply: int
#     doctor_name: Optional[str]

#     class Config:
#         from_attributes = True


# class PrescriptionCreate(PrescriptionBase):
#     pass


# class Medication(MedicationBase):
#     id: int
#     prescriptions: list[PrescriptionBase] = []

#     class Config:
#         from_attributes = True


# class Patient(PatientBase):
#     id: int
#     prescriptions: list[PrescriptionBase] = []

#     class Config:
#         from_attributes = True


# class Prescription(PrescriptionBase):
#     id: int
#     medication: MedicationBase
#     patient: PatientBase

#     class Config:
#         from_attributes = True


# Medication.model_rebuild()
# Patient.model_rebuild()
