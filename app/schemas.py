from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    # * Properties
    score: int

    class Config:
        # The lineorm_mode = True allows the app to take ORM objects and translate
        # them into responses automatically. This automation saves us from manually
        # taking data out of ORM, making it into a dictionary, then loading it in with Pydantic.
        orm_mode = True
