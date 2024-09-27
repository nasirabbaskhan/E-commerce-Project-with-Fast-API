from sqlmodel import SQLModel, Field

# from fastapi import 


class User(SQLModel, table=True):
    user_id:int | None = Field(default=None, primary_key=True)
    user_name: str
    user_email:str
    user_password:str
    phone_number:int 
    
    
class Create_User(SQLModel):
    user_name: str
    user_email:str
    user_password:str
    phone_number:int 
    
class Login_User(SQLModel):
    user_email:str
    user_password:str
    
class Update_User(SQLModel):
    user_name: str | None = None
    user_email:str | None = None
    user_password:str | None = None
    phone_number:int | None  = None