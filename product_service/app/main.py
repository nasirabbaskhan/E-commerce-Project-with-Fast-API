
import asyncio
from fastapi import FastAPI

from app.kafka.consumers import category_consume_messages, product_consume_messages, rating_consume_messages, review_consume_messages
import uvicorn
from fastapi import APIRouter
from contextlib import asynccontextmanager
from app.db.db_connectivity import create_table
from app.routes.routers import category_router, product_router, rating_router, review_router



@asynccontextmanager
async def lifespan(app=FastAPI):
    print("creating tables..")
    Task= asyncio.create_task(category_consume_messages('category', 'broker:19092'))
    Task= asyncio.create_task(product_consume_messages('product', 'broker:19092'))
    Task= asyncio.create_task(rating_consume_messages('rating', 'broker:19092'))
    Task= asyncio.create_task(review_consume_messages('reviews', 'broker:19092'))
    create_table()
    print("created table")
    yield

app= FastAPI(lifespan=lifespan,
             title="product service",
             version="1.0.0",
              description="API for managing products",)

@app.get("/")
async def rout():
    return "Welcome to Our Product Service"

#Catagory
app. include_router(router=category_router, tags=["Catagory"])
#Products
app.include_router(router=product_router, tags=["Products"])
#Review
app.include_router(router=review_router, tags=["Review"])
#Rating
app.include_router(router=rating_router, tags=["Rating"])


def start():
    uvicorn.run("app.main:app", host= "0.0.0.0", port=8085, reload=True)