from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


# Order Models
class Order(SQLModel, table=True):
    order_id: int | None = Field(default=None, primary_key=True)
    user_id: int  # This ID will be managed and validated by the User Management service
    order_date: datetime = Field(default_factory=datetime.utcnow)
    status: str
    total_amount: float

    order_items: List["OrderItem"] = Relationship(back_populates="order_item")
    shipment: Optional["Shipment"] = Relationship(back_populates="order_shipment")



class OrderAdd(SQLModel):
    user_id: int
    order_date: Optional[datetime] = None
    status: str
    total_amount: float






class OrderUpdate(SQLModel):
    status: str | None = None
    total_amount: float | None = None





# OrderItem Models
class OrderItem(SQLModel, table=True):
    order_item_id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.order_id")
    product_id: int  # Assume this is managed and validated by the Product service
    quantity: int
    price: float
    total_price: float

    order_item: Order = Relationship(back_populates="order_items")
    
    

class OrderItemAdd(SQLModel):
    order_id: int
    product_id: int
    quantity: int
    price: float
    # total_price: float


class OrderItemUpdate(SQLModel):
    quantity: int | None= None
    price: float | None = None
    total_price: float | None = None




# Shipment Models
class Shipment(SQLModel, table=True):
    shipment_id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.order_id")
    shipment_date: datetime = Field(default_factory=datetime.utcnow)
    delivery_date: Optional[datetime] = None
    status: str

    order_shipment: Order = Relationship(back_populates="shipment")
    
    

class ShipmentAdd(SQLModel):
    order_id: int
    shipment_date: Optional[datetime]
    delivery_date: Optional[datetime] = None
    status: str


class ShipmentUpdate(SQLModel):
    shipment_date: Optional[datetime] = datetime.utcnow()
    delivery_date: Optional[datetime] = datetime.utcnow()
    status: str | None = None
