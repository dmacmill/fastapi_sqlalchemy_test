from datetime import date
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app import models
from app.models import Medication, Prescription, Patient
from app.db import engine, DB_URI

import logging
import pytest

LOGGER=logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio

## HELPER
async def helper_post_patient_medication(med: Medication, patient: Patient, db_session: AsyncSession):
    # create a patient and medication first
    db_session.add(med)
    db_session.add(patient)
    await db_session.commit()
    await db_session.refresh(med)

    # check patient and medication exists
    med_object = await db_session.get(Medication, med.id)
    pat_object = await db_session.get(Patient, med.id)
    assert med_object
    assert pat_object


## TESTS
async def test_post(async_client: AsyncClient, db_session: AsyncSession):
    # create a patient and medication first
    med = Medication(name="hello", use_case="world", stock=1)
    patient = Patient(name="John Doe", phone_num="1234567890", email="john@example.com", insurance_num="98765", insurance_type="PPO")
    await helper_post_patient_medication(med, patient, db_session)

    # Post the prescription
    data={"medication_id": med.id,
          "patient_id": patient.id,
          "dose": "test_dose 100mg",
          "every": "2 per day",
          "amount": 180,
          "refills": 1,
          "last_filled": "2025-06-21",
          "day_supply": 90,
          "doctor_name": "Dr. Hibbert"}
    response = await async_client.post("/api/prescriptions/prescription", json=data)
    assert response.status_code == 200
    db_object = await db_session.get(Prescription, 1)
    assert db_object is not None


async def test_get(async_client: AsyncClient, db_session: AsyncSession):
    # setup med and patient
    med = Medication(name="hello", use_case="world", stock=1)
    patient = Patient(name="John Doe", phone_num="1234567890", email="john@example.com", insurance_num="98765", insurance_type="PPO")
    await helper_post_patient_medication(med, patient, db_session)

    # post object
    prescription = Prescription(medication_id=med.id, 
                                patient_id=patient.id, 
                                dose="test", 
                                every="2 per day", 
                                amount=180, 
                                refills=1, 
                                last_filled=date(2025, 6, 21),
                                day_supply=90,
                                doctor_name="Dr. Hibbert")
    db_session.add(prescription)
    await db_session.commit()
    await db_session.refresh(prescription)

    # get object
    response = await async_client.get(f"/api/prescriptions/prescription/{prescription.id}")
    correct_response = {
        "id": prescription.id,
        "medication_id": med.id,
        "patient_id": patient.id,
        "dose": "test",
        "every": "2 per day",
        "amount": 180,
        "refills": 1,
        "last_filled": "2025-06-21",
        "day_supply": 90,
        "doctor_name": "Dr. Hibbert",
        "medication": {
            "name":"hello",
            "use_case": "world",
            "stock": 1
        },
        "patient": {
            "name": "John Doe",
            "phone_num": "1234567890",
            "email": "john@example.com",
            "insurance_num": "98765",
            "insurance_type": "PPO"
        }
    }
    assert response.status_code == 200
    assert correct_response == response.json()


async def test_all_prescriptions(async_client: AsyncClient, db_session: AsyncSession):
    # setup meds and patients
    med1 = Medication(name="hello", use_case="world", stock=1)
    patient1 = Patient(name="John Doe", phone_num="1234567890", email="john@example.com", insurance_num="98765", insurance_type="PPO")
    await helper_post_patient_medication(med1, patient1, db_session)
    
    med2 = Medication(name="other", use_case="medicine", stock=20)
    patient2 = Patient(name="asdf asdf", phone_num="9876543210", email="asdf@example.com", insurance_num="S125463115", insurance_type="HMO")
    await helper_post_patient_medication(med2, patient2, db_session)

    # setup prescriptions
    prescription1 = Prescription(medication_id=med1.id, 
                                patient_id=patient1.id, 
                                dose="test", 
                                every="3 per day", 
                                amount=270, 
                                refills=5, 
                                last_filled=date(2025, 6, 1),
                                day_supply=90,
                                doctor_name="Dr. Octagonapus")

    prescription2 = Prescription(medication_id=med2.id, 
                                patient_id=patient1.id, 
                                dose="test", 
                                every="1 per day", 
                                amount=30, 
                                refills=0, 
                                last_filled=None,
                                day_supply=30,
                                doctor_name="Dr. Octagonapus")
    
    prescription3 = Prescription(medication_id=med2.id, 
                                patient_id=patient2.id, 
                                dose="test", 
                                every="when needed", 
                                amount=30, 
                                refills=2, 
                                last_filled=None,
                                day_supply=30,
                                doctor_name=None)
    db_session.add_all([prescription1, prescription2, prescription3])
    await db_session.commit()
    await db_session.refresh(prescription1)
    await db_session.refresh(prescription2)
    await db_session.refresh(prescription3)

    # get all
    response = await async_client.get("/api/prescriptions/all_prescriptions")
    correct_response = [
        {
            "id": prescription1.id,
            "medication_id": med1.id,
            "patient_id": patient1.id,
            "dose": "test",
            "every": "3 per day",
            "amount": 270,
            "refills": 5,
            "last_filled": "2025-06-01",
            "day_supply": 90,
            "doctor_name": "Dr. Octagonapus",
            "medication": {
                "name": "hello",
                "use_case": "world",
                "stock": 1,
                "id": med1.id
            },
            "patient": {
                "name": "John Doe",
                "phone_num": "1234567890",
                "email": "john@example.com",
                "insurance_num": "98765",
                "insurance_type": "PPO",
                "id": patient1.id
            }
        },
        {
            "id": prescription2.id,
            "medication_id": med2.id,
            "patient_id": patient1.id,
            "dose": "test",
            "every": "1 per day",
            "amount": 30,
            "refills": 0,
            "last_filled": None,
            "day_supply": 30,
            "doctor_name": "Dr. Octagonapus",
            "medication": {
                "name": "other",
                "use_case": "medicine",
                "stock": 20,
                "id": med2.id
            },
            "patient": {
                "name": "John Doe",
                "phone_num": "1234567890",
                "email": "john@example.com",
                "insurance_num": "98765",
                "insurance_type": "PPO",
                "id": patient1.id
                
            }
        },
        {
            "id": prescription3.id,
            "medication_id": med2.id,
            "patient_id": patient2.id,
            "dose": "test",
            "every": "when needed",
            "amount": 30,
            "refills": 2,
            "last_filled": None,
            "day_supply": 30,
            "doctor_name": None,
            "medication": {
                "name": "other",
                "use_case": "medicine",
                "stock": 20,
                "id": med2.id
            },
            "patient": {
                "name": "asdf asdf",
                "phone_num": "9876543210",
                "email": "asdf@example.com",
                "insurance_num": "S125463115",
                "insurance_type": "HMO",
                "id": patient2.id
            }
        }
    ]
    assert response.status_code == 200
    assert sorted(correct_response, key=lambda x: x['id']) == sorted(response.json(), key=lambda x: x['id'])

# async def test_all_prescriptions(async_client: AsyncClient, db_session: AsyncSession):
#     # create objects
#     prescription1 = Prescription(name="Alice", phone_num="1111111111", email="alice@example.com", insurance_num="11111", insurance_type="HMO")
#     prescription2 = Prescription(name="Bob", phone_num="2222222222", email="bob@example.com", insurance_num="22222", insurance_type="PPO")
#     db_session.add_all([prescription1, prescription2])
#     await db_session.commit()
#     await db_session.refresh(prescription1)
#     await db_session.refresh(prescription2)

#     # check objects exist
#     db_object1 = await db_session.get(Prescription, prescription1.id)
#     db_object2 = await db_session.get(Prescription, prescription2.id)
#     assert db_object1
#     assert db_object2

#     # get all
#     response = await async_client.get("/api/prescriptions/all_prescriptions")
#     correct_response = [
#         {
#             "name": "Alice",
#             "phone_num": "1111111111",
#             "email": "alice@example.com",
#             "insurance_num": "11111",
#             "insurance_type": "HMO",
#             "id": prescription1.id,
#             "prescriptions": []
#         },
#         {
#             "name": "Bob",
#             "phone_num": "2222222222",
#             "email": "bob@example.com",
#             "insurance_num": "22222",
#             "insurance_type": "PPO",
#             "id": prescription2.id,
#             "prescriptions": []
#         }
#     ]
#     assert response.status_code == 200
#     assert sorted(correct_response, key=lambda x: x['id']) == sorted(response.json(), key=lambda x: x['id'])

# async def test_update(async_client: AsyncClient, db_session: AsyncSession):
#     # create object
#     prescription = Prescription(name="Jane Doe", phone_num="3333333333", email="jane@example.com", insurance_num="33333", insurance_type="EPO")
#     db_session.add(prescription)
#     await db_session.commit()
#     await db_session.refresh(prescription)

#     # check object exists
#     db_object = await db_session.get(Prescription, prescription.id)
#     assert db_object

#     # update object
#     data = {
#         "name": "Jane Doe",
#         "phone_num": "3333333333",
#         "email": "jane@example.com",
#         "insurance_num": "33333",
#         "insurance_type": "POS"
#     }
#     response = await async_client.patch(f"/api/prescriptions/prescription/{prescription.id}", json=data)
#     assert response.status_code == 200
#     db_object = await db_session.get(Prescription, prescription.id)
#     assert db_object
#     assert db_object.insurance_type == "POS"

# async def test_delete(async_client: AsyncClient, db_session: AsyncSession):
#     # create object
#     prescription = Prescription(name="Mark Smith", phone_num="4444444444", email="mark@example.com", insurance_num="44444", insurance_type="HMO")
#     db_session.add(prescription)
#     await db_session.commit()
#     await db_session.refresh(prescription)

#     # check object exists
#     db_object = await db_session.get(Prescription, prescription.id)
#     assert db_object

#     # delete object
#     response = await async_client.delete(f"/api/prescriptions/prescription/{prescription.id}")
#     assert response.status_code == 200
#     db_object = await db_session.get(Prescription, prescription.id)
#     assert not db_object