import asyncio
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import select
from app.models import Feedback
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.util import greenlet_spawn
from sqlalchemy_utils import database_exists, create_database

from fastapi.testclient import TestClient

# from app.core.db import get_session
# app = FastAPI()
from app.main import app, get_db

from app.models import Base

load_dotenv()
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_ip = os.getenv('DB_IP')
db_name = os.getenv('DB_NAME') + "_test"
DATABASE_URL = "postgresql+asyncpg://{}:{}@{}/{}".format(
    db_user, db_pass, db_ip, db_name)


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    default_db = (
        "postgresql+asyncpg://{}:{}@{}/postgres".format(
            db_user, db_pass, db_ip)
    )
    test_db = DATABASE_URL
    engine = create_async_engine(default_db)

    print("engine=", engine)

    def _make_test_db():
        if not database_exists(test_db):
            create_database(test_db)

    def _make_test_tables():
        pass
        # async def init_models():
        #     async with engine.begin() as conn:
        #         await conn.run_sync(Base.metadata.drop_all)
        #         await conn.run_sync(Base.metadata.create_all)
        # await init_models()

        # Base.metadata.create_all(bind=engine)

    (await greenlet_spawn(_make_test_db))
    # (await greenlet_spawn(_make_test_tables))

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest_asyncio.fixture(scope="function")
async def db(db_engine):
    connection = await db_engine.connect()

    # begin a non-ORM transaction
    await connection.begin()

    # bind an individual Session to the connection
    Session = sessionmaker(
        bind=connection, class_=AsyncSession, autocommit=False, autoflush=False,)
    # db = Session()
    # db = Session(db_engine)

    async with Session() as session:
        yield session
        await session.rollback()

    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def db_async(db_engine):
    connection = await db_engine.connect()
    await connection.begin()
    Session = sessionmaker(
        bind=connection, class_=AsyncSession, autocommit=False, autoflush=False,)

    yield Session

    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(db_async):
    async def mock_get_db():
        async with db_async() as session:
            yield session
    #! could not make it using seperate db
    # app.dependency_overrides[get_db] = mock_get_db

    with TestClient(app) as c:
        yield c


# app.dependency_overrides[get_db] = override_get_db
# client = TestClient(app)

@pytest.mark.asyncio
async def test_create_feedback(client: TestClient, db):
    response = client.post("/feedback", json={"score": 5})

    assert response.status_code == 200
    assert response.json() == {"score": 5}

    feedback = await db.execute(select(Feedback).where(Feedback.score == 5).order_by(Feedback.id.desc()))
    
    assert feedback


@pytest.mark.asyncio
async def test_index(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
