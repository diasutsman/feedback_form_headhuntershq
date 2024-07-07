import asyncio
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import select
from fastapi.testclient import TestClient

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util import greenlet_spawn
from sqlalchemy_utils import database_exists, create_database

# Importing app, get_db, and Base from the application
from app.main import app, get_db
from app.models import Base, Feedback

# Load environment variables from a .env file
load_dotenv()

# Database configuration
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_ip = os.getenv("DB_IP")
db_name = os.getenv("DB_NAME") + "_test"
DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_ip}/{db_name}"


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    """
    Fixture to create and yield a database engine for the test session.

    This will create a test database if it doesn't exist and initialize the tables.
    """
    # Default database URL to connect and create the test database
    default_db = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_ip}/postgres"
    test_db = DATABASE_URL
    engine = create_async_engine(default_db)

    def _make_test_db():
        if not database_exists(test_db):
            create_database(test_db)

    await greenlet_spawn(_make_test_db)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest_asyncio.fixture(scope="function")
async def db(db_engine):
    """
    Fixture to provide a new database session for each test function.

    This ensures that each test function runs in isolation with a fresh transaction.
    """
    connection = await db_engine.connect()
    await connection.begin()

    Session = sessionmaker(
        bind=connection, class_=AsyncSession, autocommit=False, autoflush=False
    )

    async with Session() as session:
        yield session
        await session.rollback()

    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def db_async(db_engine):
    """
    Fixture to provide a new session maker for async database operations.

    This is used to create a new session for each test function.
    """
    connection = await db_engine.connect()
    await connection.begin()

    Session = sessionmaker(
        bind=connection, class_=AsyncSession, autocommit=False, autoflush=False
    )

    yield Session

    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(db_async):
    """
    Fixture to provide a TestClient for the FastAPI application.

    This mocks the database dependency to use the test database.
    """

    async def mock_get_db():
        async with db_async() as session:
            yield session

    with TestClient(app) as c:
        yield c


@pytest.mark.asyncio
async def test_create_feedback(client: TestClient, db):
    """
    Test case for creating a feedback entry.

    This test verifies that a feedback entry can be successfully created via the API.
    """
    response = client.post("/feedback", json={"score": 5})

    assert response.status_code == 200
    assert response.json() == {"score": 5}

    feedback = await db.execute(
        select(Feedback).where(Feedback.score == 5).order_by(Feedback.id.desc())
    )

    assert feedback is not None


@pytest.mark.asyncio
async def test_index(client: TestClient):
    """
    Test case for the index endpoint.

    This test verifies that the index endpoint returns a 200 status code.
    """
    response = client.get("/")
    assert response.status_code == 200
