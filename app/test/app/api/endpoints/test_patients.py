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


async def test_post(async_client: AsyncClient, db_session: AsyncSession):
    data={"name": "hello", "phone_num": "8675309", "email": "test@test.com", "insurance_num": "12345", "insurance_type": "HMO"}
    response = await async_client.post("/api/patients/patient", json=data)
    assert response.status_code == 200
    db_object = await db_session.get(Patient, 1)
    assert db_object is not None

async def test_get(async_client: AsyncClient, db_session: AsyncSession):
    # create object
    patient = Patient(name="John Doe", phone_num="1234567890", email="john@example.com", insurance_num="98765", insurance_type="PPO")
    db_session.add(patient)
    await db_session.commit()
    await db_session.refresh(patient)

    # check object exists
    db_object = await db_session.get(Patient, patient.id)
    assert db_object

    # get object
    response = await async_client.get(f"/api/patients/patient/{patient.id}")
    correct_response = {
        "name": "John Doe",
        "phone_num": "1234567890",
        "email": "john@example.com",
        "insurance_num": "98765",
        "insurance_type": "PPO",
        "id": patient.id,
        "prescriptions": []
    }
    assert response.status_code == 200
    assert correct_response == response.json()

async def test_all_patients(async_client: AsyncClient, db_session: AsyncSession):
    # create objects
    patient1 = Patient(name="Alice", phone_num="1111111111", email="alice@example.com", insurance_num="11111", insurance_type="HMO")
    patient2 = Patient(name="Bob", phone_num="2222222222", email="bob@example.com", insurance_num="22222", insurance_type="PPO")
    db_session.add_all([patient1, patient2])
    await db_session.commit()
    await db_session.refresh(patient1)
    await db_session.refresh(patient2)

    # check objects exist
    db_object1 = await db_session.get(Patient, patient1.id)
    db_object2 = await db_session.get(Patient, patient2.id)
    assert db_object1
    assert db_object2

    # get all
    response = await async_client.get("/api/patients/all_patients")
    correct_response = [
        {
            "name": "Alice",
            "phone_num": "1111111111",
            "email": "alice@example.com",
            "insurance_num": "11111",
            "insurance_type": "HMO",
            "id": patient1.id,
            "prescriptions": []
        },
        {
            "name": "Bob",
            "phone_num": "2222222222",
            "email": "bob@example.com",
            "insurance_num": "22222",
            "insurance_type": "PPO",
            "id": patient2.id,
            "prescriptions": []
        }
    ]
    assert response.status_code == 200
    assert sorted(correct_response, key=lambda x: x['id']) == sorted(response.json(), key=lambda x: x['id'])

async def test_update(async_client: AsyncClient, db_session: AsyncSession):
    # create object
    patient = Patient(name="Jane Doe", phone_num="3333333333", email="jane@example.com", insurance_num="33333", insurance_type="EPO")
    db_session.add(patient)
    await db_session.commit()
    await db_session.refresh(patient)

    # check object exists
    db_object = await db_session.get(Patient, patient.id)
    assert db_object

    # update object
    data = {
        "name": "Jane Doe",
        "phone_num": "3333333333",
        "email": "jane@example.com",
        "insurance_num": "33333",
        "insurance_type": "POS"
    }
    response = await async_client.patch(f"/api/patients/patient/{patient.id}", json=data)
    assert response.status_code == 200
    db_object = await db_session.get(Patient, patient.id)
    assert db_object
    assert db_object.insurance_type == "POS"

async def test_delete(async_client: AsyncClient, db_session: AsyncSession):
    # create object
    patient = Patient(name="Mark Smith", phone_num="4444444444", email="mark@example.com", insurance_num="44444", insurance_type="HMO")
    db_session.add(patient)
    await db_session.commit()
    await db_session.refresh(patient)

    # check object exists
    db_object = await db_session.get(Patient, patient.id)
    assert db_object

    # delete object
    response = await async_client.delete(f"/api/patients/patient/{patient.id}")
    assert response.status_code == 200
    db_object = await db_session.get(Patient, patient.id)
    assert not db_object