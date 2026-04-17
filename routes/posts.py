from fastapi import APIRouter,HTTPException,Query,Depends,Request
from typing import Annotated
from sqlmodel import Session, select
from models.post import *
from database import get_session
from security import *
from datetime import datetime


router = APIRouter(tags=["posts"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/posts", response_model=PostOutput)
def create_todo(post:PostInput, session: SessionDep,current_user: User = Depends(get_current_user)):
    db_post = Post(
    **post.model_dump(),
    user_id=current_user.user_id,
    created_at=datetime.now()
)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    output_post=PostOutput(
        **db_post.model_dump(),
        posted_by=session.exec(select(User).where(User.user_id==db_post.user_id)).first().user_name
    )
    return output_post

@router.get("/posts/{post_id}", response_model=PostOutput)
def read_post(post_id: int, session: SessionDep):
    post = session.exec(select(Post).where(post_id==Post.post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post does not exist")
    output_post=PostOutput(
        **post.model_dump(),
        posted_by=session.exec(select(User).where(User.user_id==post.user_id)).first().user_name
    )
    return output_post