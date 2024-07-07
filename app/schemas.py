from pydantic import BaseModel, ConfigDict


class FeedbackCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # * Properties
    score: int
