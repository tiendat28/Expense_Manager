from datetime import date as date_type, datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.models.debt import DebtType


class DebtCreate(BaseModel):
    person_name: str
    type: DebtType
    category: str = "Khác"
    total_amount: float
    paid_amount: float = 0
    due_date: Optional[date_type] = None
    note: str = ""


class DebtUpdate(DebtCreate):
    pass


class DebtPaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    amount: float
    date: datetime


class DebtRead(DebtCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    payments: List[DebtPaymentRead] = []


class DebtPayment(BaseModel):
    amount: float
    date: Optional[datetime] = None
