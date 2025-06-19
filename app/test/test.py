from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from starlette.middleware.cors import CORSMiddleware

from app.main import app
from app import models
from app.models import Medication, Prescription, Patient
from app.db import engine, DB_URI

import asyncio
import logging
import pytest
import pytest_asyncio


LOGGER=logging.getLogger(__name__)


# @pytest_asyncio.fixture(autouse=True, scope="session")
# async def run_before_and_after():
#     # this fixture doesn't start the db tables, main.py does that.

#     yield # runs the tests

#     # Cleanup the db after tests are done
#     async with engine.begin() as conn:
#         await conn.run_sync(models.Base.metadata.drop_all)


### TESTS ###
@pytest.mark.asyncio
async def test_read_main():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello world!"}

def test_database():
    """ensure connection to the test_db will work (containerized address)
    """
    assert DB_URI == "postgresql+asyncpg://postgres:postgres@db:5432/test_db"

@pytest.mark.asyncio
async def test_endpoint():
    LOGGER.warning("YEEEEEE")
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            data={"name": "hello", "use_case": "world", "stock": 1}
            response = await client.post("/api/medications/medication", json=data)
            assert response.status_code == 200