from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    score: int

    class Config:
        orm_mode = True
