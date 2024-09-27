import asyncio
from fastapi import FastAPI
from app.kafka.consumers import orderItem_consume_messages, order_consume_messages, shipment_consume_messages
import uvicorn
from contextlib import asynccontextmanager
from app.db.db_connectivity import create_table
from app.routes.order_item_routes import orderitem_router
from app.routes.order_routes import order_router
from app.routes.shipmint_routes import shipment_router



@asynccontextmanager
async def lifespan(app=FastAPI):
    print("creating tables..")
    
    create_table()
    print("created table")
    Task= asyncio.create_task(orderItem_consume_messages('orderItem', 'broker:19092'))
    Task= asyncio.create_task(order_consume_messages('order', 'broker:19092'))
    Task= asyncio.create_task(shipment_consume_messages('shipment', 'broker:19092'))
    yield

app= FastAPI(lifespan=lifespan,
             title="order service",
             version="1.0.0",
              description="API for managing orders",)

@app.get("/")
async def rout():
    return "Welcome to Our Order Service"


# Order
app.include_router(router=order_router, tags=["Order"])
# Orderitem
app.include_router(router=orderitem_router, tags=["OrderItem"])
# Shipment
app.include_router(router=shipment_router, tags=["Shipment"])

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8083, reload=True)