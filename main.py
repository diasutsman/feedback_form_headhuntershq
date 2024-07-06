from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, MetaData, inspect
from starlette.responses import FileResponse 
from sqlalchemy_utils import database_exists, create_database


db_user = 'postgres'
db_pass = '12345'
db_ip = 'localhost'
db_name = 'test_db'
DATABASE_URL = "postgresql+asyncpg://{}:{}@{}/{}/".format(db_user,db_pass,db_ip,db_name)


Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
# if not database_exists(engine.url): 
#     create_database(engine.url) # Create the database if not already created
# init_db(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
    # init db
    # await init_db(engine=engine)
    # yield

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)

class FeedbackCreate(BaseModel):
    score: int


async def get_db():
    async with SessionLocal() as session:
        yield session

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
    # run after app shutdown

async def init_db(engine):
    pass
    # if not database_exists(engine.url): 
    #     create_database(engine.url) # Create the database if not already created
    # if not inspect(engine).has_table(Feedback.__tablename__):
    #     Base.metadata.create_all(engine)

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
