from fastapi import APIRouter,HTTPException,Depends,Request
from typing import Annotated
from sqlmodel import Session, select
from models.user import *
from database import get_session
from security import *
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["authentication"])
SessionDep = Annotated[Session, Depends(get_session)]



@router.post("/users/register",response_model=UserOutput)
def register(user: UserInput,session: SessionDep):
    existing_user=session.exec(select(User).where(User.email==user.email)).first()
    if(existing_user is not None):
        raise HTTPException(status_code=400, detail="User already exists. Log in")
    hashed_password = hashPassword(user.password)
    db_user=User(
        user_name=user.user_name,
        email=user.email,
        hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/users/login")
def login(request: Request,session: SessionDep,form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user= session.exec(select(User).where(User.email==form_data.username)).first()
    if(existing_user is None):
        raise HTTPException(status_code=400,detail="user doesnt exists, signup first")
    if not verifyPassword(form_data.password,existing_user.hashed_password):
        raise HTTPException(status_code=401,detail="Incorrect password")
    else:
        return {
            "access_token":create_access_token(existing_user.user_id),
            "token_type":"bearer"
        }