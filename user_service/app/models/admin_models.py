

import uuid

from sqlmodel import Field, SQLModel


class Admin(SQLModel, table=True):
    admin_id:int | None =  Field(default=None, primary_key=True)
    admin_name:str
    admin_email:str
    admin_password:str
    admin_secret: str
    admin_kid: str = Field(default_factory=lambda: uuid.uuid4().hex)
    
class AdminCreateModel(SQLModel):
    admin_name: str
    admin_email: str
    admin_password: str
    admin_secret: str
    
    
class AdminLoginForm(SQLModel):
    admin_email: str
    admin_password: str
    admin_secret: str