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

    perscriptions: Mapped[List["Perscription"]] = relationship(back_populates="patient")


# class Medication(Base):
#     __tablename__ = "medications"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, index=True, default=True, nullable=False)
#     use_case = Column(String)
#     stock = Column(Integer, nullable=False, server_default=0)

#     perscriptions = relationship("Perscription", back_populates="perscriptions")

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, default=True, nullable=False)
    phone_num: Mapped[str] = mapped_column(default=True, nullable=False)
    email: Mapped[str] = mapped_column()
    insurance_num: Mapped[str] = mapped_column()
    insurance_type: Mapped[str] = mapped_column()

    perscriptions: Mapped[List["Perscription"]] = relationship(back_populates="patient")

# class Patient(Base):
#     __tablename__ = "patients"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, index=True, default=True, nullable=False)
#     phone_num = Column(String, default=True, nullable=False)
#     email = Column(String)
#     insurance_num = Column(String)
#     insurance_type = Column(String)

#     perscriptions = relationship("Perscription", back_populates="perscriptions")


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

# class Perscriptions(Base):
#     __tablename__ = "perscriptions"

#     id = Column(Integer, primary_key=True)
#     medication_id = Column(Integer, ForeignKey("medications.id"))
#     patient_id = Column(Integer, ForeignKey("patients.id"))
#     dose = Column(String, default=True, nullable=False)
#     every = Column(String, default=True, nullable=False)
#     amount = Column(Integer, default=True, nullable=False)
#     refills = Column(Integer, default=True, nullable=False)
#     last_filled = Column(Date)
#     day_supply = Column(Integer, nullable=False)
#     doctor_name = Column(String, default=True)

#     medication = relationship("Medication", back_populates="medications")
#     perscriptions = relationship("Perscription", back_populates="perscriptions")
