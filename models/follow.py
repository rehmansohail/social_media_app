from sqlmodel import SQLModel, Field

class FollowInput(SQLModel):
    follower: int
    followed: int

class Follow(FollowInput,table=True):
    id: int=Field(default=None,primary_key=True)

