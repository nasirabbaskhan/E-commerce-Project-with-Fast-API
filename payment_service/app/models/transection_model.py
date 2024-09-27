from datetime import datetime
from sqlmodel import Field, SQLModel



class Transaction(SQLModel, table=True):
    transaction_id: int = Field(default=None, primary_key=True)
    stripe_id: str
    user_id: int
    amount: int
    currency: str
    description: str
    status: str
    transaction_date: datetime = Field(default_factory=datetime.utcnow)

class PaymentRequest(SQLModel):
    amount: int
    currency: str
    description: str
    payment_method: str  # pm_card_visa


class PaymentUpdate(SQLModel):
    amount: int | None = None
    currency: str | None = None
    description: str | None = None
    payment_method: str | None = None  # pm_card_visa