from sqlmodel import SQLModel, Field


class LikeInput(SQLModel):
    post_id: int
    user_id: int

class Like(LikeInput,table=True):
    id: int=Field(default=None,primary_key=True)
