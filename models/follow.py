from sqlmodel import SQLModel, Field

class FollowInput(SQLModel):
    follower: int
    followed: int

class FollowOutput(SQLModel):
    follower: str
    followed: str

class Follow(FollowInput,table=True):
    id: int=Field(default=None,primary_key=True)

