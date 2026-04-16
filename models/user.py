from sqlmodel import SQLModel, Field

class UserInput(SQLModel):
    user_name: str
    email:str
    password: str
class UserOutput(SQLModel):
    user_id:int
    user_name: str
    email:str

class User(SQLModel, table=True):
    user_id: int=Field(default=None,primary_key=True)
    user_name:str=Field(index=True,unique=True)
    email:str=Field(index=True,unique=True)
    hashed_password: str