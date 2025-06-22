from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app import models
from app.models import Medication, Prescription, Patient
from app.db import engine, DB_URI

import logging
import pytest

LOGGER=logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio


async def test_read_main(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

async def test_database():
    """ensure connection to the test_db will work (containerized address)
    """
    assert DB_URI == "postgresql+asyncpg://postgres:postgres@db:5432/test_db"
