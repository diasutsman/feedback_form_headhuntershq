from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    """
    Pydantic model for creating new feedback entries.

    Attributes:
    - score: int - The score provided by the user, ranging from 1 to 5
    """

    score: int  # The score given by the user, must be an integer

    class Config:
        """
        Pydantic configuration class to enable ORM mode.

        Enabling orm_mode allows the model to be used with SQLAlchemy ORM objects.
        """
        orm_mode = True
