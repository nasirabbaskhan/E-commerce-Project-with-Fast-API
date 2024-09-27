
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# Location model
class Location(SQLModel, table=True):
    location_id:int | None = Field(default=None, primary_key=True)
    location_name: str
    address: str | None = None
    inventory_items: List["Inventory"] = Relationship(back_populates="location") # type: ignore
    
    
    
    
class LocationAdd(SQLModel):
    location_name: str
    address: str | None = None



class LocationUpdate(SQLModel):
    location_name: str | None = None
    address: str | None = None



# Inventory model
class Inventory(SQLModel, table=True):
    inventory_id: int | None = Field(default=None, primary_key=True)
    product_id: int | None   # This will reference a product ID from the Product service
    quantity: int | None 
    location_id: int | None  = Field(default=None, foreign_key="location.location_id")
    location: Optional["Location"] = Relationship(back_populates="inventory_items")
    # stock_movements: List["StockMovement"] = Relationship(back_populates="inventory")


class InventoryAdd(SQLModel):
    location_id: int | None
    product_id: int | None
    quantity: int
   

class InventoryUpdate(SQLModel):
    product_id:int | None = None
    quantity: int | None= None
    location_id: int | None= None
    
    
    
    

   