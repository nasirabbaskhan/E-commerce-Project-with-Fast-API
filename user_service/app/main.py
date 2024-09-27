import asyncio
from fastapi import FastAPI
from app.kafka.user_consumers import user_consume_messages
import uvicorn
from fastapi import APIRouter
from contextlib import asynccontextmanager
from app.db.db_connectivity import create_table
from app.routes import user_routes, admin_routes
from app.models.admin_models import Admin



@asynccontextmanager
async def lifespan(app=FastAPI):
    print("creating tables..")
    Task= asyncio.create_task(user_consume_messages('user', 'broker:19092'))
    create_table()
    print("created table")
    yield

app= FastAPI(lifespan=lifespan,
             title="User and Admin Service",
             version="1.0.0",
              description="API for managing users",)

@app.get("/")
async def rout():
    return "Welcome to )ur User Service"





app.include_router(router=user_routes.router, tags=["Users"])
app.include_router(router=admin_routes.router , tags=["Admin"])

def start():
    uvicorn.run("app.main:app", host= "0.0.0.0", port= 8086, reload=True)