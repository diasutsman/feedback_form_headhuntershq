import os
from dotenv import load_dotenv
from starlette.responses import FileResponse
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends

# Importing local modules
from app.schemas import FeedbackCreate
from app.models import Feedback

# Load environment variables from a .env file
load_dotenv()

# Database configuration
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_ip = os.getenv('DB_IP')
db_name = os.getenv('DB_NAME')

# Construct the database URL for asyncpg connection
DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_ip}/{db_name}"

# Create an asynchronous engine instance
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Dependency to get a session from the session maker


async def get_db():
    async with SessionLocal() as session:
        yield session

# Initialize the FastAPI app
app = FastAPI()

# Mount the static files directory to serve static files
app.mount("/public", StaticFiles(directory="public"), name="public")

# Define the root endpoint to serve the index.html file


@app.get("/")
async def read_index():
    return FileResponse('public/index.html')

# Define the feedback endpoint to create feedback entries


@app.post("/feedback", response_model=FeedbackCreate)
async def create_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new feedback entry in the database.

    Parameters:
    - feedback: FeedbackCreate - The feedback data from the request body
    - db: AsyncSession - The database session dependency

    Returns:
    - The created feedback entry
    """
    db_feedback = Feedback(score=feedback.score)  # Create a Feedback instance
    db.add(db_feedback)  # Add the new Feedback instance to the session
    await db.commit()  # Commit the transaction to the database
    await db.refresh(db_feedback)  # Refresh the instance to get the new ID
    return db_feedback  # Return the newly created feedback
