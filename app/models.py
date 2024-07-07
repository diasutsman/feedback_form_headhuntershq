from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

# Create a base class for declarative class definitions
Base = declarative_base()

class Feedback(Base):
    """
    Feedback model representing the 'feedback' table in the database.

    Attributes:
    - id: Integer, Primary Key - Unique identifier for each feedback entry
    - score: Integer, Not Null - Score provided by the user, ranging from 1 to 5
    """
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    score = Column(Integer, nullable=False)  # Score column, must be provided and cannot be null
