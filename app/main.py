from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.responses import FileResponse
from models import Feedback
from schemas import FeedbackCreate

from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_ip = os.getenv('DB_IP')
db_name = os.getenv('DB_NAME')
DATABASE_URL = "postgresql+asyncpg://{}:{}@{}/{}".format(
    db_user, db_pass, db_ip, db_name)


Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        yield session

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")


@app.get("/")
async def read_index():
    return FileResponse('public/index.html')


@app.post("/feedback/", response_model=FeedbackCreate)
async def create_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    db_feedback = Feedback(score=feedback.score)
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback
