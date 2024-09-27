from typing import Annotated
from aiokafka import AIOKafkaProducer # type: ignore
from fastapi import Depends, APIRouter, HTTPException

from app.controllers.payment_controllers import create_payment_intent, delete_transaction, get_transaction_id, get_transactions, update_transaction


transaction_router = APIRouter()


# Crud Transaction

@transaction_router.post("/create-payment-intent")
async def create_payment(createed_payment:Annotated[dict, Depends(create_payment_intent)]):
   if createed_payment:
        return createed_payment
   raise HTTPException(status_code=404, detail="payment is not added")


@transaction_router.get("/transactions")
def get_all_transactions(transection: Annotated[dict, Depends(get_transactions)]):
    if transection:
        return transection
    raise HTTPException(status_code=404, detail="transection is not exist")


@transaction_router.get("/transactions/{transaction_id}")
def get_transaction_by_id(transection: Annotated[dict, Depends(get_transaction_id)]):
    if transection:
        return transection
    raise HTTPException(status_code=404, detail="transection is not exist")




@transaction_router.put("/transactions_update/{transaction_id}")
def update_transaction_by_id(transection: Annotated[dict, Depends(update_transaction)]):
    if transection:
        return transection
    raise HTTPException(status_code=404, detail="transection is not updated")


@transaction_router.delete("/transactions_delete/{transaction_id}")
def delete_transaction_by_id(message: Annotated[dict, Depends(delete_transaction)]):
    if message:
        return message
    raise HTTPException(status_code=404, detail="transection has not deleted")
    
