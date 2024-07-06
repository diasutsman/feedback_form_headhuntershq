from contextlib import asynccontextmanager
import asyncpg
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer
from starlette.responses import FileResponse 
from sqlalchemy_utils import database_exists, create_database
import asyncio

db_user = 'postgres'
db_pass = '12345'
db_ip = 'localhost:5432'
db_name = 'test_db'
DATABASE_URL = "postgresql+asyncpg://{}:{}@{}/{}".format(db_user,db_pass,db_ip,db_name)


Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
# async def init_db():
    # print("Test create db if not exists")
    # await create_database(engine.url) # Create the database if not already create

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)

class FeedbackCreate(BaseModel):
    score: int

async def get_db():
    async with SessionLocal() as session:
        yield session

async def connect_create_if_not_exists(user, database):
    try:
        conn = await asyncpg.connect(user=user, database=database, password=db_pass)
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database='template1',
            user=db_user,
            password=db_pass
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{database}" OWNER "{user}"'
        )
        await sys_conn.close()

        # Connect to the newly created database.
        conn = await asyncpg.connect(user=user, database=database)

    return conn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database tables if they don't exist
    # if not await database_exist(engine.url): await create_database(engine.url)
    await connect_create_if_not_exists(db_user, db_name)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield # this is written to ensure the lifespan function is called so that all code before this is run before app runs, 
    # and all code after the `yield` will run after app finishes for releasing resources
    
app = FastAPI(lifespan=lifespan)


app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/feedback/", response_model=FeedbackCreate)
async def create_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    db_feedback = Feedback(score=feedback.score)
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback

# asyncio.run(init_db) # Here