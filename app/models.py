from datetime import date
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .db import Base


class Medication(Base):
    __tablename__ = "medications_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, default=True, nullable=False)
    use_case: Mapped[str] = mapped_column()
    stock: Mapped[int] = mapped_column(nullable=False, server_default="0")

    perscriptions: Mapped[List["Perscription"]] = relationship(back_populates="medication")

    def update(self, d):
        self.name = d["name"]
        self.use_case = d["use_case"]
        self.stock = d["stock"]


class Patient(Base):
    __tablename__ = "patients_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, default=True, nullable=False)
    phone_num: Mapped[str] = mapped_column(default=True, nullable=False)
    email: Mapped[str] = mapped_column()
    insurance_num: Mapped[str] = mapped_column()
    insurance_type: Mapped[str] = mapped_column()

    perscriptions: Mapped[List["Perscription"]] = relationship(back_populates="patient")

    def update(self, d):
        self.name = d["name"]
        self.phone_num = d["phone_num"]
        self.email = d["email"]
        self.insurance_num = d["insurance_num"]
        self.insurance_type = d["insurance_type"]


class Perscription(Base):
    __tablename__ = "perscriptions_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    medication_id: Mapped[int] = mapped_column(ForeignKey("medications_table.id"))
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients_table.id"))
    dose: Mapped[str] = mapped_column(default=True, nullable=False)
    every: Mapped[str] = mapped_column(default=True, nullable=False)
    amount: Mapped[int] = mapped_column(default=True, nullable=False)
    refills: Mapped[int] = mapped_column(default=True, nullable=False)
    last_filled: Mapped[Optional[date]]
    day_supply: Mapped[int] = mapped_column(nullable=False)
    doctor_name: Mapped[Optional[str]]

    medication: Mapped["Medication"] = relationship(back_populates="perscriptions")
    patient: Mapped["Patient"] = relationship(back_populates="perscriptions")

    def update(self, d):
        self.medication_id = d["medication_id"]
        self.patient_id = d["patient_id"]
        self.dose = d["dose"]
        self.every = d["every"]
        self.amount = d["amount"]
        self.refills = d["refills"]
        self.last_filled = d["last_filled"]
        self.day_supply = d["day_supply"]
        self.doctor_name = d["doctor_name"]