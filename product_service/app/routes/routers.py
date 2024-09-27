from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException

from app.controllers.product_controllers import  create_product, delete_product_by_id,  get_product, get_product_id, update_product_by_id
from app.models.productModel import Category, CategoryAdd, CategoryUpdate, Product, Rating, Review
from app.controllers.category_controllers import create_catagory, delete_category_by_id ,get_category, get_category_id,update_category_by_id
from app.controllers.rating_controllers import add_rating, get_rating, get_rating_id , update_rating_by_id , delete_rating_by_id
from app.controllers.review_controllers import add_review, get_review, get_review_id, update_review_by_id, delete_review_by_id



category_router = APIRouter()
product_router = APIRouter()
review_router = APIRouter()
rating_router = APIRouter()



# # Category Crud Opreation Api
@category_router.post("/add_category")
def add_category(added_catagory:Annotated[dict, Depends(create_catagory)]):
    if added_catagory:
        return added_catagory
    raise HTTPException(status_code=404, detail="Catagories not added")


@category_router.get("/get_category", response_model=List[Category])
def get_categories(all_catagory: Annotated[dict, Depends(get_category)]):
    if all_catagory:
        return all_catagory
    raise HTTPException(status_code=404, detail="Catagories not exist")


@category_router.get("/category_by_id/{category_id}",  response_model=Category)
def get_category_by_id( catagory:Annotated[dict, Depends(get_category_id)]):
    if catagory:
        return catagory
    raise HTTPException(status_code=404, detail="Catagory not exist")



@category_router.put("/category_update/{category_id}", response_model=Category)
def update_category( Updated_catagory:Annotated[dict, Depends(update_category_by_id)]):
    if Updated_catagory:
        return Updated_catagory
    raise HTTPException(status_code=404, detail="Catagory is not updataed")


@category_router.delete("/category_delete/{category_id}")
def delete_category( message: Annotated[str, Depends(delete_category_by_id)]):
    return message
    
    
    
# Product Crud opreation Api

@product_router.post("/add_product", response_model=Product)
async def add_product(added_product:Annotated[dict, Depends(create_product)]):
    if added_product:
        return added_product
    raise HTTPException(status_code=404, detail="products not added")

  
@product_router.get("/get_product", response_model=List[Product])
def get_products(products: Annotated[dict, Depends(get_product)]):
    if products:
        return products
    raise HTTPException(status_code=404, detail="products not exist")


@product_router.get("/product_by_id/{product_id}", response_model=Product)
def get_product_by_id( product: Annotated[dict, Depends(get_product_id)]):
   if product:
        return product
   raise HTTPException(status_code=404, detail="Catagory not exist") 
    

@product_router.put("/product_update/{product_id}", response_model=Product)
def update_product( updated_product: Annotated[dict, Depends(update_product_by_id)]):
    if updated_product:
        return updated_product
    raise HTTPException(status_code=404, detail="product is not updataed")


@product_router.delete("/product_delete/{product_id}")
def delete_product( message: Annotated[str, Depends(delete_product_by_id)]):
    return message



# # Rating Crud Opreation Api

@rating_router.post("/add_rating")
async def create_rating(added_rating:Annotated[dict, Depends(add_rating)]):
    if added_rating:
        return added_rating
    raise HTTPException(status_code=404, detail="rating not added")
    
        
@rating_router.get("/get_rating", response_model=List[Rating])
def get_ratings(rating: Annotated[dict, Depends(get_rating)]):
    if rating:
        return rating
    raise HTTPException(status_code=404, detail="rating not exist")


@rating_router.get("/rating_by_id/{rating_id}", response_model=Rating)
def get_rating_by_id( rating: Annotated[dict, Depends(get_rating_id)]):
    if rating:
        return rating
    raise HTTPException(status_code=404, detail="rating not exist")


@rating_router.put("/rating_update/{rating_id}", response_model=Rating)
def update_rating(updated_rating: Annotated[dict, Depends(update_rating_by_id)]):
    if updated_rating:
        return updated_rating
    raise HTTPException(status_code=404, detail="rating is not updataed")


@rating_router.delete("/rating_delete/{rating_id}")
def delete_rating( message: Annotated[str, Depends(delete_rating_by_id)]):
    return message


# # Review Crud Opreation Api

@review_router.post("/add_review")
async def create_review(added_review:Annotated[dict, Depends(add_review)]):
    if added_review:
        return added_review
    raise HTTPException(status_code=404, detail="review not added")
   
@review_router.get("/get_review", response_model=List[Review])
def get_reviews(review: Annotated[dict, Depends(get_review)]):
    if review:
        return review
    raise HTTPException(status_code=404, detail="review not exist")


@review_router.get("/review_by_id/{review_id}", response_model=Review)
def get_review_by_id( review: Annotated[dict, Depends(get_review_id)]):
    if review:
        return review
    raise HTTPException(status_code=404, detail="review not exist")




@review_router.put("/review_update/{review_id}", response_model=Review)
def update_review(updated_review: Annotated[dict, Depends(update_review_by_id)]):
    if updated_review:
        return updated_review
    raise HTTPException(status_code=404, detail="review is not updataed")


@review_router.delete("/review_delete/{review_id}")
def delete_review( message: Annotated[str, Depends(delete_review_by_id)]):
    return message
