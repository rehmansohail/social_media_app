from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session,select
from fastapi import Depends,HTTPException
from database import get_session
from typing import Annotated
from models.user import *
from dotenv import load_dotenv

SessionDep = Annotated[Session, Depends(get_session)]

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hashPassword(password: str):
    return pwd_context.hash(password)

def verifyPassword(inputPassword: str, storedPassword: str):
    return pwd_context.verify(inputPassword,storedPassword)

def create_access_token(user_id):
    data={
        "sub": str(user_id)
    }
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    data["exp"]=expire
    token = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    return token

def get_current_user(session: SessionDep,token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="No such user")
        existing_user= session.exec(select(User).where(User.user_id==user_id)).first()
        if(existing_user is None):
            raise HTTPException(status_code=401,detail="user doesnt exists, signup first")
        return existing_user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")