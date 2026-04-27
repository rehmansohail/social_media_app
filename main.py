from fastapi import FastAPI,Depends
from typing import Annotated
from contextlib import asynccontextmanager
from database import create_db_and_tables,get_session
from sqlmodel import Session
from routes.auth import router as auth_router
from routes.posts import router as post_router
from routes.likes import router as like_router
from routes.follows import router as follow_router
from routes.users import router as user_router
from routes.feed import router as feed_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app= FastAPI(lifespan=lifespan)

SessionDep = Annotated[Session, Depends(get_session)]

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(follow_router)
app.include_router(user_router)
app.include_router(feed_router)