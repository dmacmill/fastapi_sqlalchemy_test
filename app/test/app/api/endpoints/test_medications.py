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
    # LOGGER.warning("test")
    data={"name": "hello", "use_case": "world", "stock": 1}
    response = await async_client.post("/api/medications/medication", json=data)
    assert response.status_code == 200

async def test_get(async_client: AsyncClient, db_session: AsyncSession):
    # LOGGER.warning("test")
    data={"name": "hello", "use_case": "world", "stock": 1}
    response = await async_client.post("/api/medications/medication", json=data)
    response = await async_client.get("/api/medications/medication/1")
    correct_response={"name": "hello", "use_case": "world", "stock": 1, "id": 1, 'prescriptions': []}
    assert response.status_code == 200
    assert correct_response == response.json()
