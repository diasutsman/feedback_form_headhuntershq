from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    score: int

    class Config:
        from_attributes = True
