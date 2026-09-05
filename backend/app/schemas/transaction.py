from datetime import date as date_type
from pydantic import BaseModel, ConfigDict
from app.models.transaction import TransactionType


class TransactionBase(BaseModel):
    amount: float
    category: str
    note: str = ""
    date: date_type
    type: TransactionType = TransactionType.expense


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
