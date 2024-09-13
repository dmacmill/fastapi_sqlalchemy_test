from pydantic import BaseModel

from datetime import date


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
    dose: str
    every: str
    amount: int
    refills: int
    last_filled: date
    day_supply: int
    doctor_name: str

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


Medication.update_forward_refs()
Patient.update_forward_refs()

##################
###################
# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         from_attributes = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         from_attributes = True
