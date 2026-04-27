from sqlmodel import SQLModel, Field
from datetime import datetime

class PostInput(SQLModel):
    title: str
    description: str

class PostOutput(PostInput):
    post_id:int
    created_at:datetime
    posted_by: str

class Post(PostInput, table=True):
    user_id: int=Field(default=None)
    post_id: int=Field(default=None,primary_key=True)
    created_at: datetime

class PostCard(PostOutput):
    num_likes: int



