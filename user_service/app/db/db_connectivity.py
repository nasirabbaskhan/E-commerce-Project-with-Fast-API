from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from app import settings



connection_string: str = str(settings.DATABASE_URL).replace("postgresql" , "postgresql+psycopg")

engine= create_engine(connection_string, connect_args={"sslmode":"require"}, pool_recycle=300, echo=True)



# create table
def create_table():
    SQLModel.metadata.create_all(engine)
    
    
# create session
def get_session():
    with Session(engine) as session:
        yield session
        
        
# DB connector
DB_Session= Annotated[Session, Depends(get_session)]
