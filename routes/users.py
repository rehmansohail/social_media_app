from fastapi import APIRouter,HTTPException,Depends
from typing import Annotated
from sqlmodel import Session, select
from models.like import *
from models.user import *
from models.post import *
from models.follow import *
from database import get_session
from security import *
from sqlalchemy import func


router = APIRouter(tags=["users"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/users/{user_id}/followers")
def numFollowers(user_id:int, session: SessionDep):
    user_exists = session.exec(select(User).where(User.user_id==user_id)).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User does not exist")
    num_followers = session.exec(select(func.count()).where(Follow.followed == user_id)).one()
    
    return {"Number of Followers": num_followers}

@router.get("/users/{user_id}/followed")
def numFollowed(user_id:int, session: SessionDep):
    user_exists = session.exec(select(User).where(User.user_id==user_id)).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User does not exist")
    num_followed = session.exec(select(func.count()).where(Follow.follower == user_id)).one()
    
    return {"Number of Users Followed": num_followed}