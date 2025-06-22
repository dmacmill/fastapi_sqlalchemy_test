from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# ---------- Base Models ----------
class MedicationBase(BaseModel):
    name: str
    use_case: str
    stock: int

    class ConfigDict:
        from_attributes = True

class PatientBase(BaseModel):
    name: str
    phone_num: str
    email: str
    insurance_num: str
    insurance_type: str

    class ConfigDict:
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

    class ConfigDict:
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

    class ConfigDict:
        from_attributes = True

class Medication(MedicationBase):
    id: int
    prescriptions: List[PrescriptionSummary] = []

    class ConfigDict:
        from_attributes = True

class Patient(PatientBase):
    id: int
    prescriptions: List[PrescriptionSummary] = []

    class ConfigDict:
        from_attributes = True


# ---------- Slimmed Models without prescriptions list (for /prescription endpoint) ----------

class MedicationSlim(MedicationBase):
    id: int

    class ConfigDict:
        from_attributes = True

class PatientSlim(PatientBase):
    id: int

    class ConfigDict:
        from_attributes = True

class Prescription(PrescriptionBase):
    id: int
    medication: MedicationSlim
    patient: PatientSlim

    class ConfigDict:
        from_attributes = True
