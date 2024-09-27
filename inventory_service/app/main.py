import asyncio
from fastapi import FastAPI
import uvicorn
from fastapi import APIRouter
from contextlib import asynccontextmanager
from app.db.db_connectivity import create_table
from app.routes.inventory_routers import inventory_router
from app.routes.location_routers import location_router
from app.kafka.consumers import location_consume_messages, inventory_consume_messages



@asynccontextmanager
async def lifespan(app=FastAPI):
    print("creating tables..")
    # Task= asyncio.create_task(user_consume_messages('user', 'broker:19092'))
    create_table()
    print("created table")
    print("Starting Consumers....")
    Task= asyncio.create_task(location_consume_messages('location', 'broker:19092'))
    Task= asyncio.create_task(inventory_consume_messages('inventory', 'broker:19092'))
    
    yield

app= FastAPI(lifespan=lifespan,
             title="Inventory service",
             version="1.0.0",
              description="API for managing Inventory",)

@app.get("/")
async def rout():
    return "Welcome to Our Inventory Service"

# Location
app.include_router(router=location_router, tags=["Location"])
# Inventory
app.include_router(router=inventory_router, tags=["Inventory"])


def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8081, reload=True)