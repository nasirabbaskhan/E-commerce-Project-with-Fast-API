
from fastapi import FastAPI
import uvicorn
from fastapi import APIRouter
from contextlib import asynccontextmanager
from app.db.db_connectivity import create_table
from app.routes.transection_routes import transaction_router





@asynccontextmanager
async def lifespan(app=FastAPI):
    print("creating tables..")
    # Task= asyncio.create_task(user_consume_messages('user', 'broker:19092'))
    create_table()
    print("created table")
    print("Starting Consumers....")
   
    
    yield

app= FastAPI(lifespan=lifespan,
             title="payment service",
             version="1.0.0",
              description="API for managing payment",)

@app.get("/")
async def rout():
    return "Welcome to our payment Service"

app.include_router(router=transaction_router, tags=["Transaction"])


def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8084, reload=True)