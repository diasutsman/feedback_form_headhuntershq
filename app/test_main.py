import pytest
from sqlalchemy.util import greenlet_spawn
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from main import DATABASE_URL, app, get_db
from models import Base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = DATABASE_URL
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:12345@localhost:5432/test_multitudex_db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = None

# Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
async def db_engine():
    default_db = (
        SQLALCHEMY_DATABASE_URL
    )
    test_db = SQLALCHEMY_DATABASE_URL
    engine = create_async_engine(default_db)
    global TestingSessionLocal
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

    def _make_test_db():
        if not database_exists(test_db):
            create_database(test_db)

    def _make_test_tables():
        Base.metadata.create_all(bind=engine)

    await greenlet_spawn(_make_test_db)
    await greenlet_spawn(_make_test_tables)
    yield engine


def _make_test_db():
    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)
    create_database(SQLALCHEMY_DATABASE_URL)


def _drop_test_db():
    drop_database(SQLALCHEMY_DATABASE_URL)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_feedback():
    response = client.post("/feedback/", json={"score": 5})
    assert response.status_code == 200
    assert response.json() == {"score": 5}
