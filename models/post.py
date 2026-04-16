from sqlmodel import SQLModel, Field
from datetime import datetime

class PostInput(SQLModel):
    user_id: int
    title: str
    description: str

class Post(PostInput, table=True):
    post_id: int=Field(default=None,primary_key=True)
    created_at: datetime


