from fastapi import APIRouter,HTTPException,Query,Depends,Request
from typing import Annotated
from sqlmodel import Session, select
from models.like import *
from models.user import *
from models.post import *
from database import get_session
from security import *
from datetime import datetime


router = APIRouter(tags=["likes"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/posts/{post_id}/like", response_model=LikeOutput)
def like(post_id:int, session: SessionDep,current_user: User = Depends(get_current_user)):
    user =current_user.user_id
    username = current_user.user_name
    already_exists = session.exec(select(Post).where(Post.post_id==post_id)).first()
    if not already_exists:
        raise HTTPException(status_code=404, detail="Post does not exist")
    already_liked = session.exec(select(Like).where(Like.post_id==post_id, Like.user_id==user)).first()
    if already_liked:
        raise HTTPException(status_code=400, detail="Post already liked")
    like_db=Like(
        user_id=user,
        post_id=post_id
    )
    
    session.add(like_db)
    session.commit()
    session.refresh(like_db)
    output_like=LikeOutput(
        **like_db.model_dump(),
        liked_by=username
    )
    return output_like