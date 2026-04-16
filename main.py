from fastapi import FastAPI,Depends
from typing import Annotated
from contextlib import asynccontextmanager
from database import create_db_and_tables,get_session
from sqlmodel import Session
from routes.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app= FastAPI(lifespan=lifespan)

SessionDep = Annotated[Session, Depends(get_session)]

app.include_router(auth_router)