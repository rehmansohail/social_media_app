from sqlmodel import SQLModel, create_engine, Session


database_url = "sqlite:///./test.db"

engine = create_engine(database_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session