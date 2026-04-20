from sqlmodel import SQLModel, Field


class LikeInput(SQLModel):
    post_id: int
    user_id: int

class LikeOutput(SQLModel):
    post_id: int
    liked_by: str #username of user who liked the post

class Like(LikeInput,table=True):
    id: int=Field(default=None,primary_key=True)
