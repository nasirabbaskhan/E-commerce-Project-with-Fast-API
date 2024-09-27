from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from typing import  Annotated, List
from datetime import datetime

class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    product_category: "Product" = Relationship(back_populates="category")
    
    
class CategoryAdd(SQLModel):
    name: str
    description: str


class CategoryUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
   


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    price: float
    available: bool = True
    brand: str 
    weight: float 
    sku: str 
    category_id: int | None = Field(default=None, foreign_key="category.id")
    category: "Category" = Relationship(back_populates="product_category")
    reviews: list["Review"] = Relationship(back_populates="product_review")
    ratings: list["Rating"] = Relationship(back_populates="product_rating")
    product_images: list["ProductImage"]= Relationship(back_populates="product_item")
    
class ProductAdd(SQLModel):
    name: str
    description: str
    price: float
    category_id: int
    available: bool
    brand: str 
    weight: float 
    sku: str 

class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category_id: int | None = None
    available: bool | None = None
    brand: str | None = None
    weight: float | None = None
    sku: str | None = None
    

    
class Review(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    review_text: str
    product_id: int | None = Field(default=None, foreign_key="product.id")
    product_review: "Product" = Relationship(back_populates="reviews")
    
    
class ReviewAdd(SQLModel):
    review_text: str
    product_id: int
   
   
class ReviewUpdate(SQLModel):
    review_text: str | None = None
    

class Rating(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    rating: int
    product_id: int | None = Field(default=None, foreign_key="product.id")
    product_rating: "Product" = Relationship(back_populates="ratings")
    
class RatingAdd(SQLModel):
    rating: int
    product_id: int
  
class RatingUpdate(SQLModel):
    rating: int | None = None
   
   
class ProductImage(SQLModel, table=True):
    product_image_id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    # URL of the product item image
    product_image_url: str
    # Many-to-one relationship with ProductItem
    product_item: "Product"  = Relationship(
        back_populates="product_images")