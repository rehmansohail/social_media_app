from fastapi import APIRouter,HTTPException,Depends,Query
from typing import Annotated
from sqlmodel import Session, select
from models.like import *
from models.user import *
from models.post import *
from models.follow import *
from database import get_session
from security import *
from sqlalchemy import func


router = APIRouter(tags=["feed"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/feed", response_model=list[PostCard])
def feed(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=10)] = 10,
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.user_id
    people_followed = session.exec(select(Follow.followed).where(Follow.follower == user_id)).all()
    posts=[]
    if not people_followed:
        posts = session.exec(
            select(Post).order_by(Post.created_at.desc()).limit(limit).offset(offset)
        ).all()
        
    else:
        posts = session.exec(select(Post).where(Post.user_id.in_(people_followed)).order_by(Post.created_at.desc()).limit(limit).offset(offset)).all()
        
    feed=[]
    for post in posts:
        output_post=PostCard(
        **post.model_dump(),
        posted_by=session.exec(select(User).where(User.user_id==post.user_id)).first().user_name,
        num_likes=session.exec(select(func.count()).where(Like.post_id == post.post_id)).one()
        )
        feed.append(output_post)
    return feed
    
    