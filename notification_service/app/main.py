import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.db.db_connectivity import create_table
from app.routes.notification_routes import notification_router
from app.kafka.consumers import notification_consume_messages

# from router import *
# import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables....")
    create_table()
    print("Tables Created....")
    
    print("Starting Consumers....")
    Task= asyncio.create_task(notification_consume_messages('notification', 'broker:19092'))
  
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan, title="Notification Service", root_path="/notification"
)


@app.get("/")
def root():
    return {"message": "Hello World From Notification Service"}

# Notification
app.include_router(router=notification_router, tags=["Notification"])

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8082, reload=True)