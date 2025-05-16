from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from starlette.middleware.cors import CORSMiddleware

from app.main import app
from app import models
from app.models import Medication, Prescription, Patient
from app.db import engine, DB_URI

import logging
LOGGER=logging.getLogger(__name__)

import pytest

# cleanup the tables after the tests are all done
@pytest.fixture(autouse=True, scope="function")
async def run_before_and_after():
    async with engine.begin() as conn:
        conn.run_sync(models.Base.metadata.create_all)
    LOGGER.warning("before the fixtureeeeeeeeeeeeeeeeeeeeeeee")

    yield # run the tests

    # stuff running after yield is running after the tests are done
    # async with engine.begin() as conn:
    #     conn.run_sync(models.Base.metadata.drop_all)
    LOGGER.warning("after the fixtureeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")


### TESTS
@pytest.mark.asyncio
async def test_read_main():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello world!"}

def test_database():
    assert DB_URI == "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"

@pytest.mark.asyncio
async def test_endpoint():
    LOGGER.warning("YEEEEEE")
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            data={"name": "hello", "use_case": "world", "stock": 1}
            response = await client.post("/api/medications/medication", json=data)
            assert response.status_code == 200