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


router = APIRouter(tags=["follows"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/follows/{followed_id}/follow", response_model=FollowOutput)
def follow(followed_id:int, session: SessionDep,current_user: User = Depends(get_current_user)):
    user =current_user.user_id
    username=current_user.user_name
    if(user==followed_id):
        raise HTTPException(status_code=400, detail="You cant follow yourself")
    user_exists = session.exec(select(User).where(User.user_id==followed_id)).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User does not exist")
    already_followed = session.exec(select(Follow).where(Follow.followed==followed_id, Follow.follower==user)).first()
    if already_followed:
        raise HTTPException(status_code=400, detail="User is already followed")
    follow_db=Follow(
        follower=user,
        followed=followed_id
    )
    
    session.add(follow_db)
    session.commit()
    session.refresh(follow_db)

    followed_user=session.exec(select(User).where(User.user_id==followed_id)).first()
    follow_output=FollowOutput(
        follower=username,
        followed=followed_user.user_name
    )
    
    return follow_output


@router.delete("/follows/{followed_id}/unfollow")
def unfollow(followed_id: int, session: SessionDep,current_user: User = Depends(get_current_user)):
    user =current_user.user_id
    if(user==followed_id):
        raise HTTPException(status_code=400, detail="You cant unfollow yourself")
    user_exists = session.exec(select(User).where(User.user_id==followed_id)).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User does not exist")
    already_followed = session.exec(select(Follow).where(Follow.follower==user, Follow.followed==followed_id)).first()
    if not already_followed:
        raise HTTPException(status_code=400, detail="User not Followed yet")
    session.delete(already_followed)
    
    session.commit()
    return {"Success": "User Unfollowed"}

