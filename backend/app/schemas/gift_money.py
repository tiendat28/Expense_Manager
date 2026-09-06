from datetime import date
from pydantic import BaseModel, ConfigDict
from app.models.gift_money import GiftMoneyType


class GiftMoneyCreate(BaseModel):
    name: str
    address: str = ""
    amount: float
    type: GiftMoneyType
    date: date
    note: str = ""


class GiftMoneyUpdate(GiftMoneyCreate):
    pass


class GiftMoneyRead(GiftMoneyCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
