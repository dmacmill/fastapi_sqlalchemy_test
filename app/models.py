from datetime import date
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .db import Base


class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, default=True, nullable=False)
    use_case: Mapped[str] = mapped_column()
    stock: Mapped[int] = mapped_column(nullable=False, server_default="0")

    perscriptions: Mapped[List["Perscription"]] = relationship(back_populates="patient", lazy="selectin")


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, default=True, nullable=False)
    phone_num: Mapped[str] = mapped_column(default=True, nullable=False)
    email: Mapped[str] = mapped_column()
    insurance_num: Mapped[str] = mapped_column()
    insurance_type: Mapped[str] = mapped_column()

    perscriptions: Mapped[List["Perscription"]] = relationship(back_populates="patient", lazy="selectin")


class Perscription(Base):
    __tablename__ = "perscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    medication_id: Mapped[int] = mapped_column(ForeignKey("medications.id"))
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    dose: Mapped[str] = mapped_column(default=True, nullable=False)
    every: Mapped[str] = mapped_column(default=True, nullable=False)
    amount: Mapped[int] = mapped_column(default=True, nullable=False)
    refills: Mapped[int] = mapped_column(default=True, nullable=False)
    last_filled: Mapped[date] = mapped_column()
    day_supply: Mapped[int] = mapped_column(nullable=False)
    doctor_name: Mapped[str] = mapped_column(default=True)

    medication: Mapped["Medication"] = relationship(back_populates="perscriptions")
    patient: Mapped["Patient"] = relationship(back_populates="perscriptions")