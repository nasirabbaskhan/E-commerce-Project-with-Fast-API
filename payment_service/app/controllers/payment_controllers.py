import os
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.db.db_connectivity import get_session
from app.models.transection_model import PaymentRequest, PaymentUpdate, Transaction
import stripe # type: ignore

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


async def create_payment_intent(
    payment_request: PaymentRequest, session:Annotated[Session, Depends(get_session)], user_id: int):
    try:
        
            # Create a payment method first
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "4242424242424242",  # Test card number
                "exp_month": 12,
                "exp_year": 2024,
                "cvc": "123",
            },
        )
    
        # Create a payment intent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=payment_request.amount,
            currency=payment_request.currency,
            description=payment_request.description,
            payment_method=payment_method.id,  # Use the valid payment method ID
            confirm=True,
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
            metadata={"user_id": str(user_id)},
        )

        # Store the transaction in the database
        transaction = Transaction(
            stripe_id=intent.id,
            user_id=user_id,
            amount=intent.amount,
            currency=intent.currency,
            description=intent.description,
            status=intent.status,
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return {"status": "success", "payment_intent": transaction}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_transactions(session:Annotated[Session, Depends(get_session)]):
    try:
        transaction = session.exec(select(Transaction)).all()
        if transaction:
            return transaction
        raise HTTPException(status_code=404, detail="Transaction not found")    
        
    except Exception as e:
        return {"error": str(e)}


def get_transaction_id(transaction_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Transaction, transaction_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



def update_transaction(transaction_id: int, transaction_update: PaymentUpdate, session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Transaction, transaction_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        update_data = transaction_update.model_dump(exclude_unset=True)
        get_data.sqlmodel_update(update_data)
        session.add(get_data)
        session.commit()
        session.refresh(get_data)
        return get_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def delete_transaction(transaction_id: int, session:Annotated[Session, Depends(get_session)]):
    try:
        get_data = session.get(Transaction, transaction_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        session.delete(get_data)
        session.commit()
        return {"message": "Transaction Deleted Successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
