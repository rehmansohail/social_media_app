from sqlmodel import SQLModel, create_engine, Session
from models.follow import Follow
from models.like import Like
from models.post import Post
from models.user import User


database_url = "sqlite:///./test.db"

engine = create_engine(database_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session