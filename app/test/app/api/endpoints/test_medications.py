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
    data={"name": "hello", "use_case": "world", "stock": 1}
    response = await async_client.post("/api/medications/medication", json=data)
    assert response.status_code == 200
    db_object = await db_session.get(Medication, 1)
    assert db_object is not None

async def test_get(async_client: AsyncClient, db_session: AsyncSession):
    # create object
    med = Medication(name="hello", use_case="world", stock=1)
    db_session.add(med)
    await db_session.commit()
    await db_session.refresh(med)

    # check object exists
    db_object = await db_session.get(Medication, 1)
    assert db_object

    # get object
    response = await async_client.get("/api/medications/medication/1")
    correct_response={"name": "hello", "use_case": "world", "stock": 1, "id": 1, 'prescriptions': []}
    assert response.status_code == 200
    assert correct_response == response.json()

async def test_all_medications(async_client: AsyncClient, db_session: AsyncSession):
    # create objects
    med1 = Medication(name="one", use_case="one", stock=1)
    med2 = Medication(name="two", use_case="two", stock=1)
    db_session.add_all([med1, med2])
    await db_session.commit()
    await db_session.refresh(med1)
    await db_session.refresh(med2)

    # check objects exist
    db_object1 = await db_session.get(Medication, med1.id)
    db_object2 = await db_session.get(Medication, med2.id)
    assert db_object1
    assert db_object2

    # get all
    response = await async_client.get("/api/medications/all_medications")
    correct_response = [
        {"name": "one", "use_case": "one", "stock": 1, "id": med1.id, 'prescriptions': []},
        {"name": "two", "use_case": "two", "stock": 1, "id": med2.id, 'prescriptions': []}
    ]
    assert response.status_code == 200
    assert sorted(correct_response, key=lambda x: x['id']) == sorted(response.json(), key=lambda x: x['id'])

async def test_update(async_client: AsyncClient, db_session: AsyncSession):
    # create object
    med = Medication(name="hello", use_case="world", stock=1)
    db_session.add(med)
    await db_session.commit()
    await db_session.refresh(med)

    # check object exists
    db_object = await db_session.get(Medication, 1)
    assert db_object

    # update object
    data={"name": "hello", "use_case": "world", "stock": 100}
    response = await async_client.patch("/api/medications/medication/1", json=data)
    assert response.status_code == 200
    db_object = await db_session.get(Medication, 1)
    assert db_object
    assert db_object.stock == 100

async def test_delete(async_client: AsyncClient, db_session: AsyncSession):
    # create object
    med = Medication(name="hello", use_case="world", stock=1)
    db_session.add(med)
    await db_session.commit()
    await db_session.refresh(med)

    # check object exists
    db_object = await db_session.get(Medication, 1)
    assert db_object

    # delete object
    response = await async_client.delete("/api/medications/medication/1")
    assert response.status_code == 200
    db_object = await db_session.get(Medication, 1)
    assert not db_object