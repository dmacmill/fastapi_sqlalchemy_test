import asyncio
import pytest
import pytest_asyncio
import warnings

from fastapi import FastAPI
from typing import AsyncGenerator, Generator, Callable
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, Generator, Callable

from app.models import Base
from app.db import AsyncSessionLocal, engine

# A more conventional conftest setup for async from 
# https://rogulski.it/blog/sqlalchemy-14-async-orm-with-fastapi/


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    """
    Create an instance of the default event loop for each test case.
    Needed because the event loop will otherwise be hogged by asyncio.
    """
    warnings.filterwarnings("ignore",
                            message=".*event_loop fixture provided by pytest-asyncio*",
                            category=DeprecationWarning,
                            module="pytest_asyncio.plugin")
    
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """fixture to give tests db_session variable. session currently 
    drops the table per function call.

    Returns:
        AsyncGenerator[AsyncSession, None]: connection to db
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with AsyncSessionLocal(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest_asyncio.fixture()
async def override_get_db(db_session: AsyncGenerator[AsyncSession, None]) -> Callable:
    """Provide a function call to obtain the db session

    Args:
        db_session (AsyncGenerator[AsyncSession, None]): db_session generator (becomes AsyncSession)

    Returns:
        Callable: the way FastAPI can get the db session
    """
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture()
def app(override_get_db: Callable) -> FastAPI:
    """Replaces non-test way of getting db with the test db

    Args:
        override_get_db (Callable): function to get db_session (resolve to AsyncSession)

    Returns:
        FastAPI: new FastAPI app
    """
    from app.db import get_db
    from app.main import app

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    """Fixture to give tests an async api client.

    Args:
        app (FastAPI): where we can get the api client

    Returns:
        AsyncGenerator: yields and becomes AsyncClient
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac