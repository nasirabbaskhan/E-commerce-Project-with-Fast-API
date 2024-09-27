from sqlmodel import Field, SQLModel


class Notification(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int   # it pretent recieve from user service
    order_id: int  # # it pretent recieve from orderservice
    message: str
    read: bool = False
    
    
    
class NotificationAdd(SQLModel):
    user_id: int
    order_id: int
    message: str
    read: bool = False



class NotificationUpdate(SQLModel):
    message: str | None = None
    read: bool  = False
   