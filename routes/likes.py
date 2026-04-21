from fastapi import APIRouter,HTTPException,Depends
from typing import Annotated
from sqlmodel import Session, select
from models.like import *
from models.user import *
from models.post import *
from database import get_session
from security import *
from sqlalchemy import func


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

@router.delete("/posts/{post_id}/unlike")
def unlike(post_id:int, session: SessionDep,current_user: User = Depends(get_current_user)):
    user =current_user.user_id
    post_exists = session.exec(select(Post).where(Post.post_id==post_id)).first()
    if not post_exists:
        raise HTTPException(status_code=404, detail="Post does not exist")
    already_liked = session.exec(select(Like).where(Like.post_id==post_id, Like.user_id==user)).first()
    if not already_liked:
        raise HTTPException(status_code=400, detail="Post not liked yet")
    session.delete(already_liked)
    
    session.commit()
    return {"Success": "Post Unliked"}
    

@router.get("/posts/{post_id}/likes")
def numLikes(post_id:int, session: SessionDep):
    post_exists = session.exec(select(Post).where(Post.post_id==post_id)).first()
    if not post_exists:
        raise HTTPException(status_code=404, detail="Post does not exist")
    num_likes = session.exec(select(func.count()).where(Like.post_id == post_id)).one()
    
    return {"Number of Likes": num_likes}