from typing import Optional
from pydantic import BaseModel, ConfigDict


class BillCreate(BaseModel):
    name: str
    amount: float
    category: str = "Hóa đơn"
    due_day: int


class BillUpdate(BillCreate):
    pass


class BillRead(BillCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    last_paid_month: Optional[str] = None
